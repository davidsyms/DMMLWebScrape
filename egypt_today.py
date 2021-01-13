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

filename = "Egypt Today.csv"
with open(filename, 'w') as file: 
        csvwriter = csv.writer(file) 
        csvwriter.writerow(headers) 

for keyword in keywords:
    print("Scanning Egypt Today for {}".format(keyword))

    url_link = "https://www.egypttoday.com/Article/Search?title={}".format(keyword).replace(" ", "-")

    driver = webdriver.Firefox()
    driver.get(url_link)
    
    while(1):
        soup = BeautifulSoup(driver.page_source, "html.parser")
        try:
            last_box_text = soup.find_all("div", {"class": "BOrderBoxSection"})[-1].get_text()
        except:
            break

        if ("2020" or "2021" in last_box_text):
            try:
                page_height = driver.execute_script("return document.body.scrollHeight")
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
                driver.find_element_by_xpath("//*[@id=\"LoadMore\"]").click()
            except:
                break
        else:
            break

    soup = BeautifulSoup(driver.page_source, "html.parser")
    article_containers = soup.find_all("div", {"class": "BOrderBoxSection"})
    driver.quit()

    for i in article_containers:
        if ("2020" in i.find("span").get_text()):
            urls.append(["https://www.egypttoday.com/{}".format(i.find("h3").find("a").get("href")), "Egypt Today", keyword, "egypttoday.com"])

for url in urls:
    print("Scrapping: {}".format(url[0]))

    try:
        r = requests.get(url[0])
        soup = BeautifulSoup(r.content, "html.parser")
        headline, article, author, date = "", "", "", ""

        headline = soup.find("h1", {"class": "ArticleTitleH1"}).get_text()

        article = soup.find("div", {"class": "ArticleDescription"}).get_text()

        try:
            author = soup.find("div", {"class": "BYName"}).get_text()
        except:
            author = "No Author"

        try:
            date = soup.find("div", {"class": "Date"}).get_text().split(",")[1].split("-")[0]
        except:
            date = "No date"

        csv_values = [" ".join(headline.split()), " ".join(article.split()), " ".join(author.split()), url[2], "".join(url[0]), "".join(date), url[3]]

        with open(filename, 'a') as file: 
            csvwriter = csv.writer(file) 
            csvwriter.writerow(csv_values)
    except:
        print("Failed to scrape: {}".format(url[0]))
        continue

