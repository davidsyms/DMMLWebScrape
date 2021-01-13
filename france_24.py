from bs4 import BeautifulSoup
import requests
import csv

#############################################################################################
#                               Global Variable Declarations                                #
#############################################################################################

headers = ["Headline", "Body", "Author", "Topic label", "URL of the news article", "Published date", "Domain"]
keywords = ["Climate Change", "COVID 19", "Military Ground Vehicles"]

filename = "France 24.csv"
with open(filename, 'w') as file: 
        csvwriter = csv.writer(file) 
        csvwriter.writerow(headers) 

urls = []
waste_url = []

for keyword in keywords:
    print("Scanning France24 for {}".format(keyword))

    web_address = ""
    page = 0
    changed = 1
    while (changed):
        page += 1
        changed = 0

        if (keyword == "Climate Change"):
            if (page > 1):
                web_address = "https://www.france24.com/en/tag/climate/{}/".format(page)
            else:
                web_address = "https://www.france24.com/en/tag/climate/"
        elif (keyword == "COVID 19"):
            if (page > 1):
                web_address = "https://www.france24.com/en/tag/coronavirus/{}/".format(page)
            else:
                web_address = "https://www.france24.com/en/tag/coronavirus/"
        elif (keyword == "Military Ground Vehicles"):
            if (page > 1):
                web_address = "https://www.france24.com/en/tag/war/{}/".format(page)
            else:
                web_address = "https://www.france24.com/en/tag/war/"

        print(web_address)

        r = requests.get(web_address, headers={'User-Agent': 'Mozilla/5.0'})
        soup = BeautifulSoup(r.content, "html.parser")
        #Handles cases where there are no articles on page 

        article_containers = soup.find_all("div", {"class": "m-item-list-article"})

        for i in article_containers:
            if ("2020" in i.text):
                url_text = "https://www.france24.com{}".format(i.find("a").get("href"))
                if "tv-shows" not in url_text and "video" not in url_text:
                    urls.append([url_text, "France 24", keyword, "france24.com"])
                changed = 1

            elif ("2021" in i.text):
                url_text = "https://www.france24.com{}".format(i.find("a").get("href"))
                if url_text not in waste_url:
                    waste_url.append(url_text)
                    changed = 1
                else:
                    continue

for url in urls:
    print("Scrapping: {}".format(url[0]))
    try:
        r = requests.get(url[0])
        soup = BeautifulSoup(r.content, "html.parser")
        headline, article, author, date = "", "", "", ""

        r = requests.get(url[0], headers={'User-Agent': 'Mozilla/5.0'})
        soup = BeautifulSoup(r.content, "html.parser")

        file_index = 5

        headline = soup.find("h1", {"class": "t-content__title a-page-title"}).get_text()

        try: 
            author = soup.find("a", {"class": "m-from-author__name"}).get_text()
        except:
            author = "No Author"

        textdiv = soup.find("div", {"class": "t-content__body u-clearfix"})
        
        #Removes all children div's this included the extra links at bottom of article 
        try:
            for remove in textdiv.find_all("div"):
                remove.decompose()
            text = textdiv.find_all("p")
        except:
            continue #if ths runs there is an error textdiv doesn't exit

        article = ""
        for i in text:
            article += i.text

        date = soup.find("time").get_text()[:10]

        csv_values = [" ".join(headline.split()), " ".join(article.split()), " ".join(author.split()), url[2], "".join(url[0]), "".join(date), url[3]]

        with open(filename, 'a') as file: 
            csvwriter = csv.writer(file) 
            csvwriter.writerow(csv_values)
    except:
        print("Failed to scrape: {}".format(url[0]))
        continue