from bs4 import BeautifulSoup
import requests
from selenium import webdriver
import csv
import time
#############################################################################################
#                               Global Variable Declarations                                #
#############################################################################################

headers = ["Headline", "Body", "Author", "Topic label", "URL of the news article", "Published date", "Domain"]
keywords = ["Climate Change", "COVID 19", "Military Ground Vehicles"]
keywords = ["Climate Change"]
urls = []
waste_url = []


filename = "21st Century Wire.csv"
with open(filename, 'w') as file: 
        csvwriter = csv.writer(file) 
        csvwriter.writerow(headers) 


for keyword in keywords:
    print("Scanning 21st Century Wire for {}".format(keyword))

    if (keyword == "Climate Change"):
        url_link = "https://duckduckgo.com/?q=Climate+Change+site%3Ahttps%3A%2F%2F21stcenturywire.com&kx=%23CC9900&k9=%23CC9900&df=2020-01-01..2020-12-31&ia=web"
    if (keyword == "COVID 19"):
        url_link = "https://duckduckgo.com/?q=COVID-19+site%3Ahttps%3A%2F%2F21stcenturywire.com&kx=%23CC9900&k9=%23CC9900&df=2020-01-01..2020-12-31&ia=web"
    if (keyword == "Military Ground Vehicles"):
        url_link = "https://duckduckgo.com/?q=Military+Ground+Vehicles+site%3Ahttps%3A%2F%2F21stcenturywire.com&kx=%23CC9900&k9=%23CC9900&df=2020-01-01..2020-12-31&ia=web"

    driver = webdriver.Firefox()
    driver.get(url_link)

    while (1):
        time.sleep(3)
        page_height = driver.execute_script("return document.body.scrollHeight")
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
        time.sleep(1)
        
        try:
            driver.find_element_by_css_selector('.result--more__btn').click()
        except:
            break

    page_source = driver.page_source

    driver.quit()

    soup = BeautifulSoup(page_source, "html.parser")

    for article in soup.find_all("a", {"class": "result__url js-result-extras-url"}):
        urls.append([article.get("href"), "21st Century Wire", keyword, "21stcenturywire.com"])


for url in urls:
    print("Scrapping: {}".format(url[0]))
    try:
        r = requests.get(url[0], headers={'User-Agent': 'Mozilla/5.0'})
        soup = BeautifulSoup(r.content, "html.parser")
        headline, article, author, date = "", "", "", ""

        try:
            headline = soup.find("h1").get_text()
        except:
            print("No headline")
            continue

        try:
            article = ""
            for i in soup.find("div", {"class": "entry-content"}).find_all("p")[2:]:
                article += i.get_text()
        except:
            print("No article")
            continue
        
        try:
            author = soup.find("div", {"class": "entry-content"}).find("strong").get_text()
            print(author)
        except:
            print("No author")
            author = "no author"

        try:
            date = soup.find("div", {"class": "entry-content"}).find("strong").findNext("a").get_text()
            print(date)
        except:
            print("No date")
            date = "no date"

        csv_values = [" ".join(headline.split()), " ".join(article.split()), " ".join(author.split()), url[2], "".join(url[0]), "".join(date), url[3]]

        with open(filename, 'a') as file: 
            csvwriter = csv.writer(file) 
            csvwriter.writerow(csv_values)
            
    except:
        print("Failed to scrape: {}".format(url[0]))
        continue