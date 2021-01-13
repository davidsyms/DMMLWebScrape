from bs4 import BeautifulSoup
import requests
import csv

#############################################################################################
#                               Global Variable Declarations                                #
#############################################################################################

headers = ["Headline", "Body", "Author", "Topic label", "URL of the news article", "Published date", "Domain"]
keywords = ["Climate Change", "COVID 19", "Military Ground Vehicles"]

filename = "Times of India.csv"
with open(filename, 'w') as file: 
        csvwriter = csv.writer(file) 
        csvwriter.writerow(headers) 

urls = []


for keyword in keywords:
    print("Scanning Times of India for {}".format(keyword))

    page = 0
    changed = 1
    while (changed):
        page += 1
        changed = 0
        web_addresses = []
        
        if (keyword == "Climate Change"):
            web_addresses.append("https://timesofindia.indiatimes.com/topic/climate-change/{}".format(page))

        #Times of india has a covid landing page and multiple subpages per location. This is all the sublocations 
        elif (keyword == "COVID 19"):
            if (page > 1):
                web_addresses.append("https://timesofindia.indiatimes.com/coronavirus/india/{}".format(page))
                web_addresses.append("https://timesofindia.indiatimes.com/coronavirus/india/delhi/{}".format(page))
                web_addresses.append("https://timesofindia.indiatimes.com/coronavirus/india/bangalore/{}".format(page))
                web_addresses.append("https://timesofindia.indiatimes.com/coronavirus/india/hyderabad/{}".format(page))
                web_addresses.append("https://timesofindia.indiatimes.com/coronavirus/india/kolkata/{}".format(page))
                web_addresses.append("https://timesofindia.indiatimes.com/coronavirus/india/mumbai/{}".format(page))
                web_addresses.append("https://timesofindia.indiatimes.com/coronavirus/world/{}".format(page))
            else:
                web_addresses.append("https://timesofindia.indiatimes.com/coronavirus/india/")
                web_addresses.append("https://timesofindia.indiatimes.com/coronavirus/india/delhi/")
                web_addresses.append("https://timesofindia.indiatimes.com/coronavirus/india/bangalore/")
                web_addresses.append("https://timesofindia.indiatimes.com/coronavirus/india/hyderabad/")
                web_addresses.append("https://timesofindia.indiatimes.com/coronavirus/india/kolkata/")
                web_addresses.append("https://timesofindia.indiatimes.com/coronavirus/india/mumbai/")
                web_addresses.append("https://timesofindia.indiatimes.com/coronavirus/world/")
        elif (keyword == "Military Ground Vehicles"):
            web_addresses.append("https://timesofindia.indiatimes.com/topic/Military-Ground-Vehicles/{}".format(page))


        for web_address in web_addresses:
            print(web_address)
            r = requests.get(web_address)
            soup = BeautifulSoup(r.content, "html.parser")

            if (keyword != "COVID 19"):
                article_containers = soup.find_all("li", {"class": "article"})
            else:
                article_containers = soup.find("ul", {"class": "list5 clearfix"}).find_all("span", {"class": "w_tle"})

            for i in article_containers:
                if (keyword == "COVID 19"):
                    url_text = "https://timesofindia.indiatimes.com{}".format(i.find("a").get("href"))
                    url = [url_text, "Times of India", keyword, "timesofindia.indiatimes.com"]
                    if url not in urls:
                        urls.append(url)
                        changed = 1
                else:
                    if ("2020" in i.text):
                        url_text = "https://timesofindia.indiatimes.com{}".format(i.find("a").get("href"))
                        url = [url_text, "Times of India", keyword, "timesofindia.indiatimes.com"]
                        if url not in urls:
                            urls.append(url)
                            changed = 1

for url in urls:
    print("Scrapping: {}".format(url[0]))
    try:
        r = requests.get(url[0])
        soup = BeautifulSoup(r.content, "html.parser")
        headline, article, author, date = "", "", "", ""

        r = requests.get(url[0], headers={'User-Agent': 'Mozilla/5.0'})
        soup = BeautifulSoup(r.content, "html.parser")

        file_index = 6

        headline = soup.find("h1").get_text()

        #The date/author line varried by artcile by always had "byline" in the class this finds that line.
        #In said line the date and author was sometimes seperated by a "|" or "/" this splits the line regardless
        date_author = soup.select('div[class*="byline"]')[0].get_text().split("|")
        if(len(date_author) < 2): #this runs if the date/author is split by /
            date_author = date_author[0].split("/")

        #Author always comes first
        author = date_author[0]

        #by default assume date is second elment in split array. 
        #However, sometimes there is a second news source in which case the date index is updated
        date_index = 1
        if (len(date_author) > 2):
            date_index = 2
        try:
            if ("Updated" in date_author[date_index]):
                date_split = date_author[date_index].split(":")
                date = date_split[1][:-4].lstrip() #isolated actual date
            else:
                date_split = date_author[date_index].split(":")
                date = date_split[0][:-4].lstrip()
        except:
            date = "No Date"

        #Article saved under two different tags depending on artcile 
        try:
            article = soup.find("div", {"class": "ga-headlines"}).get_text()
        except:
            try:
                article = soup.find("div", {"class": "Normal"}).get_text()
            except:
                continue

        csv_values = [" ".join(headline.split()), " ".join(article.split()), " ".join(author.split()), url[2], "".join(url[0]), "".join(date), url[3]]

        with open(filename, 'a') as file: 
            csvwriter = csv.writer(file) 
            csvwriter.writerow(csv_values)
    except:
        print("Failed to scrape: {}".format(url[0]))
        continue