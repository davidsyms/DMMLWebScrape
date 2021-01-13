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

filename = "Taipei Times.csv"
with open(filename, 'w') as file: 
        csvwriter = csv.writer(file) 
        csvwriter.writerow(headers) 

for keyword in keywords:
    print("Scanning Taipei Times for {}".format(keyword))

    url_link = "https://www.taipeitimes.com/News/list?section=all&reportrange=January%201,%202020%20-%20December%2031,%202020&keywords={}".format(keyword)
    selenium_sleep_time = 3

    # get web page
    driver.get(url_link)
    # execute script to scroll down the page
    while (1):
        page_height = driver.execute_script("return document.body.scrollHeight")
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
        time.sleep(selenium_sleep_time)
        if (driver.execute_script("return document.body.scrollHeight") == page_height):
            break

    page_source = driver.page_source

    driver.quit()

    soup = BeautifulSoup(page_source, "html.parser")

    for article in soup.find_all("a", {"class": "tit"}):
        urls.append([article.get("href"), "Taipei Times", keyword, "taipeitimes.com"])

for url in urls:
    print("Scrapping: {}".format(url[0]))
    try:
        r = requests.get(url[0])
        soup = BeautifulSoup(r.content, "html.parser")
        headline, article, author, date = "", "", "", ""

        headline = soup.find("div", {"class": "archives"}).find("h1").get_text()

        article = ""
        text = soup.find("div", {"class": "archives"}).find_all("p")
        for i in text:
            article += i.get_text()
        
        author = soup.find("ul", {"class": "as boxTitle boxText"}).get_text().split("/")[0].replace("By", "")

        date = soup.find("h6").get_text().split("page")[0]

        csv_values = [" ".join(headline.split()), " ".join(article.split()), " ".join(author.split()), url[2], "".join(url[0]), "".join(date), url[3]]

        with open(filename, 'a') as file: 
            csvwriter = csv.writer(file) 
            csvwriter.writerow(csv_values)
            
    except:
        print("Failed to scrape: {}".format(url[0]))
        continue