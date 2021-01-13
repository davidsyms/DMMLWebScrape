from bs4 import BeautifulSoup
from selenium import webdriver
import requests
import csv
import time
#############################################################################################
#                               Global Variable Declarations                                #
#############################################################################################

headers = ["Headline", "Body", "Author", "Topic label", "URL of the news article", "Published date", "Domain"]
keywords = ["Climate Change", "COVID 19", "Military Ground Vehicles"]

urls = []
waste_url = []

filename = "Russia Today.csv"
with open(filename, 'w') as file: 
        csvwriter = csv.writer(file) 
        csvwriter.writerow(headers) 

for keyword in keywords:
    print("Scanning Russia Today for {}".format(keyword))

    web_address = ""
    page = 0
    changed = 1
    while (changed):

        page += 1
        changed = 0
        web_address = "https://www.rt.com/search?category=&df=&dt=&format=&page={}&pageSize=0&q={}&type=&xcategory=".format(page, keyword)
        
        print(web_address)

        r = requests.get(web_address, headers={'User-Agent': 'Mozilla/5.0'})
        soup = BeautifulSoup(r.content, "html.parser")
        #Handles cases where there are no articles on page 

        article_containers = soup.find_all("li", {"class": "card-list__item card-list__item_margin_bottom"})

        for i in article_containers:
            if ("2020" in i.text):
                url_text = "https://www.rt.com/{}".format(i.find("a").get("href")) 
                url = [url_text, "Russia Today", keyword, "rt.com"]
                if url not in urls:
                    urls.append(url)
                    changed = 1
            elif ("2021" in i.text):
                url_text = "https://www.rt.com/{}".format(i.find("a").get("href"))
                if url_text not in waste_url:
                    waste_url.append(url_text)
                    changed = 1

for url in urls:
    print("Scrapping: {}".format(url[0]))
    try:
        r = requests.get(url[0])
        soup = BeautifulSoup(r.content, "html.parser")
        headline, article, author, date = "", "", "", ""

        try:
            headline = soup.find("h1", {"class": "article__heading"}).get_text()
        except:
            continue

        try:
            article_text = soup.find("div", {"class": "article__text"}).find_all("p")
            for i in article_text:
                article += i.get_text()
        except:
            continue

        try:
            author = soup.find("div", {"class": "article__author-text"}).get_text()[3:].split(",")[0]
        except:
            author = "No author"

        try:
            date = soup.find("span", {"class": "date date_article-header"}).get_text()
        except:
            date = "No Date"

        csv_values = [" ".join(headline.split()), " ".join(article.split()), " ".join(author.split()), url[2], "".join(url[0]), "".join(date.split()), url[3]]

        with open(filename, 'a') as file: 
            csvwriter = csv.writer(file) 
            csvwriter.writerow(csv_values)
    except:
        print("Failed to scrape: {}".format(url[0]))
        continue