from bs4 import BeautifulSoup
import requests
import csv

#############################################################################################
#                               Global Variable Declarations                                #
#############################################################################################

headers = ["Headline", "Body", "Author", "Topic label", "URL of the news article", "Published date", "Domain"]
keywords = ["Climate Change", "COVID 19", "Military Ground Vehicles"]

filename = "TRT World.csv"
with open(filename, 'w') as file: 
        csvwriter = csv.writer(file) 
        csvwriter.writerow(headers) 

urls = []
waste_url = []

for keyword in keywords:
    print("Scanning TRT World for {}".format(keyword))

    web_address = ""
    page = 0
    changed = 1
    while (changed):
        page += 1
        changed = 0

        if (keyword == "Climate Change"):
            web_address = "https://www.trtworld.com/search?_token=ULZOsWJ0Jsm2clD0XZAJd5tjQwADEPGPYGKpSv2D&query=Climate+Change&order=published_date&date=custom&startDate=2020-01-01&endDate=2020-12-31&type=news"
        elif (keyword == "COVID 19"):
            web_address = "https://www.trtworld.com/search?_token=ULZOsWJ0Jsm2clD0XZAJd5tjQwADEPGPYGKpSv2D&query=COVID-19&order=published_date&date=custom&startDate=2020-01-01&endDate=2020-12-31&type=news"
        elif (keyword == "Military Ground Vehicles"):
            web_address = "https://www.trtworld.com/search?_token=ULZOsWJ0Jsm2clD0XZAJd5tjQwADEPGPYGKpSv2D&query=Military+Ground+Vehicles&order=published_date&date=custom&startDate=2020-01-01&endDate=2020-12-31&type=news&page={}".format(page)


        r = requests.get(web_address, headers={'User-Agent': 'Mozilla/5.0'})
        soup = BeautifulSoup(r.content, "html.parser")
        #Handles cases where there are no articles on page 

        article_containers = soup.find_all("div", {"class": "col-xs-12 latestArticle no-gutters bg-w item"})

        for i in article_containers:
            url = ["https://www.trtworld.com/{}".format(i.find("div", {"class": "caption"}).find("a").get("href")), "TRT World", keyword, "trtworld.com"]
            if url not in urls:
                changed = 1
                urls.append(url)

for url in urls:
    print("Scrapping: {}".format(url[0]))

    try:
        r = requests.get(url[0])
        soup = BeautifulSoup(r.content, "html.parser")
        headline, article, author, date = "", "", "", ""

        headline = soup.find("h1", {"class": "article-title"}).get_text()

        article = ""
        for i in soup.find("div", {"class": "contentBox bg-w noMedia"}).find_all("p"):
            article += i.get_text()

        try:
            author = soup.find("div", {"class": "article-source"}).get_text()[9:]
        except:
            author = "No Author"

        try:
            date = soup.find("ul", {"class": "author"}).get_text()
        except:
            date = "No date"

        csv_values = [" ".join(headline.split()), " ".join(article.split()), " ".join(author.split()), url[2], "".join(url[0]), "".join(date.split()), url[3]]

        with open(filename, 'a') as file: 
            csvwriter = csv.writer(file) 
            csvwriter.writerow(csv_values)
    except:
        print("Failed to scrape: {}".format(url[0]))
        continue