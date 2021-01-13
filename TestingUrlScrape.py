from bs4 import BeautifulSoup
import requests
from selenium import webdriver
import time

keywords = ["Climate Change", "COVID 19", "Military Ground Vehicles"]
urls = []

url_link = "https://www.straitstimes.com/search?searchkey=Climate Change"

driver = webdriver.Firefox()

driver.get(url_link)

while (1):
    time.sleep(.5)
    soup = BeautifulSoup(driver.page_source, "html.parser")
    if ("2020" in soup.get_text()):
        article_containers = soup.find_all("div", {"class", "queryly_item_row"})
        for article in article_containers:
            if ("2020" in article.get_text()):
                urls.append(article.find("a").get("href"))
    elif (soup.find("2021")):
        pass
    else:
        break

    try:
        driver.find_element_by_css_selector('#resultdata > a:nth-child(22)').click()
    except:
        break


    


print(urls)