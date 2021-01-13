from bs4 import BeautifulSoup
import requests
from selenium import webdriver
import csv

#############################################################################################
#                               Global Variable Declarations                                #
#############################################################################################

headers = ["Headline", "Body", "Author", "Topic label", "URL of the news article", "Published date", "Domain"]
keywords = ["Climate Change", "COVID 19", "Military Ground Vehicles"]
urls = []
waste_url = []


filename = "Straits Times.cvs"
with open(filename, 'w') as file: 
        csvwriter = csv.writer(file) 
        csvwriter.writerow(headers) 


for keyword in keywords:
    print("Scanning Straits Times for {}".format(keyword))
    url_link = "https://www.straitstimes.com/search?searchkey={}".format(keyword)

    driver = webdriver.Firefox()
    driver.get(url_link)
    changed = 1

    while (changed):
        changed = 0
        soup = BeautifulSoup(driver.page_source, "html.parser")
        article_containers = soup.find_all("div", {"class", "queryly_item_row"})
        for i in article_containers:
            if ("2020" in i.text and i.find("a").get("href") not in urls):
                url = [i.find("a").get("href"), "Straits Times", keyword, "straitstimes.com"]
                urls.append(url)
                changed = 1
            elif ("2021" in i.text and i not in waste_url):
                waste_url.append(i)
                changed = 1

        #reached end of pages
        try:
            driver.find_element_by_css_selector('#resultdata > a:nth-child(22)').click()
        except:
            break

    driver.quit()

waste_url = [] #saves memory

for url in urls:
    print("Scrapping: {}".format(url[0]))
    try:
        driver = webdriver.Firefox()
        driver.get(url[0])
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

        csv_values = [" ".join(headline.split()), " ".join(article.split()), " ".join(author.split()), url[2], "".join(url[0]), "".join(date), url[3]]

        with open(filename, 'a') as file: 
            csvwriter = csv.writer(file) 
            csvwriter.writerow(csv_values)
    except:
        print("Failed to scrape: {}".format(url[0]))
        continue
