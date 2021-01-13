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
urls = []
waste_url = []


filename = "Global Times.csv"
with open(filename, 'w') as file: 
        csvwriter = csv.writer(file) 
        csvwriter.writerow(headers) 


for keyword in keywords:
    print("Scanning Global Times for {}".format(keyword))
    url_link = "https://search.globaltimes.cn/QuickSearchCtrl?search_txt={}".format(keyword.replace(" ", "+"))

    driver = webdriver.Firefox()
    driver.get(url_link)
    changed = 1

    time.sleep(1)

    while (changed):
        changed = 0
        soup = BeautifulSoup(driver.page_source, "html.parser")
        article_containers = soup.find_all("div", {"class", "row-fluid"})
        for i in article_containers:
            if ("2020" in i.text):
                print(i.find("a").get("href"))
                url = [i.find("a").get("href"), "Global Times", keyword, "globaltimes.cn"]
                urls.append(url)
                changed = 1
            elif ("2021" in i.text and i not in waste_url):
                waste_url.append(i)
                changed = 1

        #reached end of pages
        try:
            page_height = driver.execute_script("return document.body.scrollHeight")
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
            driver.find_element_by_xpath('/html/body/div[5]/div[1]/div[12]/a[10]').click()
        except:
            break

    driver.quit()