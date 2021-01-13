from bs4 import BeautifulSoup
import requests
import csv

#############################################################################################
#                               Global Variable Declarations                                #
#############################################################################################

"""NOTE BBC WEBSITE NO LONGER SHOWS ARTICLES FROM 2020 WHEN COVID 19 IS SEARCHED"""

headers = ["Headline", "Body", "Author", "Topic label", "URL of the news article", "Published date", "Domain"]
keywords = ["Climate Change", "COVID 19", "Military Ground Vehicles"]

filename = "British Broadcasting Company.csv"
with open(filename, 'w') as file: 
        csvwriter = csv.writer(file) 
        csvwriter.writerow(headers) 

urls = []
waste_url = []


for keyword in keywords:
    print("Scanning BBC for {}".format(keyword))

    page = 0
    changed = 1

    while (changed):
        page += 1
        changed = 0

        print("https://www.bbc.co.uk/search?q={}&page={}".format(keyword, page).replace(" ", "%20"))

        r = requests.get("https://www.bbc.co.uk/search?q={}&page={}".format(keyword, page).replace(" ", "%20"))      
        soup = BeautifulSoup(r.content, "html.parser")

        #Handles cases where there are no articles on page 
        try:
            article_containers = soup.find("ul", {"class": "css-1lb37cz-Stack e1y4nx260"}).find_all("li")
        except:
            article_containers = []

        print(len(article_containers))

        for i in article_containers:
            if ("2020" in i.text):
                date = i.find("span", {"class": "css-1hizfh0-MetadataSnippet ecn1o5v0"}).find("span", {"aria-hidden": "false"}).get_text()
                
                #Since in article if it is recent it will say "2 days ago" instead of the date, so I pass the date from search page to article scrapper
                url_text = "{}*{}".format(i.find("a").get("href"), date)
                if (not "news" in url_text or "newsround" in url_text):
                    continue
                url = [url_text, "British Broadcasting Company", keyword, "bbc.co.uk"]
                if url not in urls:
                    changed = 1
                    urls.append(url)
            
            elif ("2021" in i.text):
                url_text = i.find("a").get("href")
                if url_text in waste_url:
                    continue
                else:
                    waste_url.append(url_text)
                    changed = 1


for url in urls:
    print("Scrapping: {}".format(url[0]))
    try:
        r = requests.get(url[0])
        soup = BeautifulSoup(r.content, "html.parser")
        headline, article, author, date = "", "", "", ""

        #save url that has date and updates the real url[0] again.
        date_url = "".join(url[0]).split("*")
        url[0] = date_url[0]

        r = requests.get(url[0])
        soup = BeautifulSoup(r.content, "html.parser")

        #from search can not tell if text based news or video. If a url fails any of these tests it is a news video and isnt scrapped
        try:
            file_index = 3

            headline = soup.find("h1", {"id": "main-heading"}).get_text()

            author = soup.find("p", {"class": "css-1pjc44v-Contributor e5xb54n0"}).find("strong").get_text()[3:]  

            text = soup.find_all("div", {"data-component": "text-block"})
            article = ""

            date = date_url[1]

            for i in text:
                article += i.get_text()

        except:
            continue

        csv_values = [" ".join(headline.split()), " ".join(article.split()), " ".join(author.split()), url[2], "".join(url[0]), "".join(date), url[3]]

        with open(filename, 'a') as file: 
            csvwriter = csv.writer(file) 
            csvwriter.writerow(csv_values)

    except:
        print("Failed to scrape: {}".format(url[0]))
        continue
    