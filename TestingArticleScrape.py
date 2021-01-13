from bs4 import BeautifulSoup
import requests
from selenium import webdriver
import time

"""def read_articles(urls):
    for url in urls:
        driver = webdriver.Firefox()
        driver.get(url)
        soup = BeautifulSoup(driver.page_source, "html.parser")
        driver.close()
        headline, article, author, date = "", "", "", ""

        headline = soup.find("h1", {"itemprop": "headline"}).get_text()

        textdiv = soup.find("div", {"itemprop": "articleBody"})
    
        #Removes all children div's this included the extra links at bottom of article 
        try:
            for remove in textdiv.find_all("div"):
                remove.decompose()
            text = textdiv.find_all("p")
            for i in text:
                article += i.get_text()
        except:
            continue #if ths runs there is an error textdiv doesn't exit
        
        try:
            author = soup.find("div", {"itemprop": "name"}).get_text()
        except:
            author = "No Author"

        try:
            date = soup.find("li", {"class": "story-postdate"}).get_text().split("Published")[1]
        except:
            date = "No Date"

        print("Headline:{}\narticle:{}\nauthor:{}\ndate:{}".format(headline, article, author, date))

urls = ["https://www.straitstimes.com/world/united-states/taiwan-in-talks-to-make-first-purchase-of-sophisticated-us-drones-sources", "https://www.straitstimes.com/world/united-states/military-confronts-protesters-in-us-capital", "https://www.straitstimes.com/world/united-states/taiwan-in-talks-to-make-first-purchase-of-sophisticated-us-drones-sources"]
read_articles(urls)"""

r = requests.get("https://www.egypttoday.com//Article/1/83253/Family-of-1st-Egyptian-doctor-dies-of-COVID-19-tests")
soup = BeautifulSoup(r.content, "html.parser")
headline, article, author, date = "", "", "", ""

print(soup.find("div", {"class": "Date"}).get_text().split(",")[1].split("-")[0])