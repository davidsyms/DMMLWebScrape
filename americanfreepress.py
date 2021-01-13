from bs4 import BeautifulSoup
import requests
import csv

#############################################################################################
#                               Global Variable Declarations                                #
#############################################################################################

headers = ["Headline", "Body", "Author", "Topic label", "URL of the news article", "Published date", "Domain"]
keywords = ["Climate Change", "COVID 19", "Military Ground Vehicles"]


filename = "American Free Press.csv"
with open(filename, 'w') as file: 
        csvwriter = csv.writer(file) 
        csvwriter.writerow(headers) 

urls = []
waste_url = []

for keyword in keywords:
    print("Scanning American Free Press for {}".format(keyword))

    page = 0
    changed = 1
    while (changed):
        page += 1
        changed = 0

        url_request = "https://americanfreepress.net/page/{}/?s={}".format(page, keyword).replace(" ", "+")
        r = requests.get(url_request)        
        soup = BeautifulSoup(r.content, "html.parser")

        #Handles cases where there are no articles on page 
        try:
            article_containers = soup.find_all("article")
        except:
            article_containers = []

        for i in article_containers:
            if ("2020" in i.text):
                url = [i.find("a").get("href"), "American Free Press", keyword, "americanfreepress.net"]
                if url not in urls:
                    changed = 1
                    urls.append(url)
            elif ("2021" in i.text):
                url_text = i.find("a").get("href")
                if url_text not in waste_url:
                    waste_url.append(url_text)
                    changed = 1


for url in urls:
    print("Scrapping: {}".format(url[0]))
    try:
        r = requests.get(url[0], headers={'User-Agent': 'Mozilla/5.0'})
        soup = BeautifulSoup(r.content, "html.parser")
        headline, article, author, date = "", "", "", ""

        headline = soup.find("h1", {"class": "entry-title"}).get_text() #Gets headline
        print(headline)

        #Removes all children div's this included the extra links at bottom of article 
        textdiv = soup.find("div", {"class": "entry-content clearfix"})
        
        try:
            for remove in textdiv.find_all("div"):
                remove.decompose()
        except:
            pass

        #Gets Article
        text = textdiv.find_all("p")
        article = ""
        for i in text[1:]:
            article += i.get_text()

        author = text[0].get_text()[3:]

        #Date was nestled among other things within same "i" tag. This isolates the date.
        date = soup.find("span", {"class": "entry-meta-date updated"}).find("a").get_text()

        csv_values = [" ".join(headline.split()), " ".join(article.split()), " ".join(author.split()), url[2], "".join(url[0]), "".join(date), url[3]]

        with open(filename, 'a') as file: 
            csvwriter = csv.writer(file) 
            csvwriter.writerow(csv_values)
    except:
        print("Failed to scrape: {}".format(url[0]))
        continue
