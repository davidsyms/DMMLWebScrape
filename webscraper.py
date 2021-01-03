from bs4 import BeautifulSoup
import requests
import csv

#############################################################################################
#                               Global Variable Declarations                                #
#############################################################################################

headers = ["Headline", "Body", "Author", "Topic label", "URL of the news article", "Published date", "Domain"]
keywords = ["Climate Change", "COVID 19", "Military Ground Vehicles"]

news_sites = ["Ceasefire", "Canadian Dimension", "Al Jazeera", "British Broadcasting Company", "Taipei Times", "France 24", "Times of India",
"Straits Times", "Egypt Today", "TRT World", "Russia Today", "Global Times", "21st Century Wire", "American Free Press"]

file_counter = [-1] * len(news_sites)

#Writes headers to all files
for current_news_site in range(len(news_sites)):
    filename = news_sites[current_news_site]
    with open(filename, 'w') as file: 
        csvwriter = csv.writer(file) 
        csvwriter.writerow(headers) 

#Scape Articles and pulls headline, author, date, and the article
def read_articles(urls):
    file_index = -1

    for url in urls:
        r = requests.get(url[0])
        soup = BeautifulSoup(r.content, "html.parser")
        headline, article, author, date = "", "", "", ""

        if (url[1] == "Ceasefire"):
            file_index = 0
            file_counter[file_index] += 1
            
            headline = soup.find("h1", {"itemprop": "name headline"}).get_text() #Gets headline

            #Removes all children div's this included the extra links at bottom of article 
            textdiv = soup.find("div", {"id": "entry"})
            for remove in textdiv.find_all("div"):
                remove.decompose()
           
            #Gets Article
            text = textdiv.find_all("p")
            article = ""
            for i in text[1:]:
                article += i.get_text()

            author = text[0].get_text()[3:]

            #Date was nestled among other things within same "i" tag. This isolates the date.
            date_unstripped = soup.find("div", {"class": "column_main"}).find("i").get_text()
            date = date_unstripped[14: date_unstripped[2:].find("-")+1]    

    
        elif (url[1] == "Canadian Dimension"):
            file_index = 1
            file_counter[file_index] += 1

            headline = soup.find("h1", {"class": "article-title"}).get_text()

            #author and date stored in same <p> tag, seperated by a "/". This seperates date and author
            author_date_line = soup.find("p", {"class", "byline"}).get_text().split("/")

            author = author_date_line[0]

            textdiv = soup.find("div", {"class": "content"})

            #Removes all children div's this included the extra links at bottom of article 
            for remove in textdiv.find_all("div"):
                remove.decompose()
            text = textdiv.find_all("p")

            article = ""
            for i in text:
                article += i.get_text()

            date = author_date_line[1]

        elif (url[1] == "Al Jazeera"):
            file_index = 2
            file_counter[file_index] += 1
            
            headline = soup.find("h1").get_text()

            author = "No Author"

            textdiv = soup.find("div", {"class": "wysiwyg wysiwyg--all-content"})
            
            #Removes all children div's this included the extra links at bottom of article 
            try:
                for remove in textdiv.find_all("div"):
                    remove.decompose()
                text = textdiv.find_all("p")
            except:
                continue #if ths runs there is an error textdiv doesn't exit
                

            article = ""
            for i in text:
                article += i.get_text()

            date = soup.find("div", {"class" : "date-simple"}).get_text()
            

        elif (url[1] == "British Broadcasting Company"):
            #save url that has date and updates the real url[0] again.
            date_url = "".join(url[0]).split("*")
            url[0] = date_url[0]

            r = requests.get(url[0])
            soup = BeautifulSoup(r.content, "html.parser")

            #from search can not tell if text based news or video. If a url fails any of these tests it is a news video and isnt scrapped
            try:
                file_index = 3
                file_counter[file_index] += 1

                headline = soup.find("h1", {"id": "main-heading"}).get_text()

                author = soup.find("p", {"class": "css-1pjc44v-Contributor e5xb54n0"}).find("strong").get_text()[3:]  

                text = soup.find_all("div", {"data-component": "text-block"})
                article = ""

                date = date_url[1]

                for i in text:
                    article += i.get_text()

            except:
                continue

        elif (url[1] == "France 24"):
            r = requests.get(url[0], headers={'User-Agent': 'Mozilla/5.0'})
            soup = BeautifulSoup(r.content, "html.parser")

            file_index = 4
            file_counter[file_index] += 1

            headline = soup.find("h1", {"class": "t-content__title a-page-title"}).get_text()

            try: 
                author = soup.find("a", {"class": "m-from-author__name"}).get_text()
            except:
                author = "No Author"

            textdiv = soup.find("div", {"class": "t-content__body u-clearfix"})
            
            #Removes all children div's this included the extra links at bottom of article 
            try:
                for remove in textdiv.find_all("div"):
                    remove.decompose()
                text = textdiv.find_all("p")
            except:
                continue #if ths runs there is an error textdiv doesn't exit

            article = ""
            for i in text:
                article += i.text

            date = soup.find("time").get_text()[:10]

        elif(url[1] == "Times of India"):
            r = requests.get(url[0], headers={'User-Agent': 'Mozilla/5.0'})
            soup = BeautifulSoup(r.content, "html.parser")

            file_index = 5
            file_counter[file_index] += 1

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
            
        #Combines all values into one list for csv writing 
        csv_values = [" ".join(headline.split()), " ".join(article.split()), " ".join(author.split()), url[2], "".join(url[0]), "".join(date), url[3]]
        filename = news_sites[file_index]

        #Writes to csv
        with open(filename, 'a') as file: 
            csvwriter = csv.writer(file) 
            csvwriter.writerow(csv_values)


urls = []

for keyword in keywords:

    #############################################################################################
    #                                  Ceasefire                                                #
    #############################################################################################
    print("Scanning Ceasefire for {}".format(keyword))

    #open searche url and create soup
    r = requests.get("https://ceasefiremagazine.co.uk/?s={}".format(keyword.replace(" ", "+")))
    soup = BeautifulSoup(r.content, "html.parser")

    #finds all URLs from year 2020 
    article_containers = soup.find_all("div", {"id": "featured_w"})
    
    for i in article_containers:
        if ("2020" in i.find("h2").find("i").contents[0]):
            urls.append([i.find("h1").find("a").get("href"), "Ceasefire", keyword, "ceasefiremagazine.co.uk"])

    #############################################################################################
    #                                  Canadian Dimension                                       #
    #   Notes:  Since this news sites has multiple pages ("next" button) per result I use a     #
    #           loop to iteratively search each "next" page until no articles from 2020 are     #
    #           found                                                                           #
    #############################################################################################
    print("Scanning Canadian Dimension for {}".format(keyword))

    #There are multiple pages on this site, these variables are used to iterate through the pages
    web_address = ""
    page = 0
    changed = 1
    while (changed):
        changed = 0

        #Canadian Dimension has certain pages for environment and COVID. It does not for MGV. Therefore,
        #Uses CD's default search tool to locate articles.
        # *****NOTE: after a sizeable amount of requests CD search will switch to a custom google search*******
        if (keyword == "Climate Change"):
            web_address = "https://canadiandimension.com/articles/category/environment/P{}0".format(page)
        elif (keyword == "COVID 19"):
            web_address = "https://canadiandimension.com/articles/category/covid-19/P{}0".format(page)
        elif (keyword == "Military Ground Vehicles"):
            web_address = "https://canadiandimension.com/search/973c007b780e3452f8d8b15a63648590/P{}0".format(page)

        r = requests.get(web_address)
        soup = BeautifulSoup(r.content, "html.parser")

        #Handles cases where there are no articles on page 
        try:
            article_containers = soup.find_all("li")
        except:
            article_containers = []

        for i in article_containers:
            if ("2020" in i.text):
                urls.append([i.find("a").get("href"), "Canadian Dimension", keyword, "canadiandimension.com"])
                changed = 1
                page += 1

    #############################################################################################
    #                                  Al Jazeera                                               #
    #############################################################################################
    print("Scanning Al Jazeera for {}".format(keyword))

    page = 0
    changed = 1
    while (changed):
        page += 1
        changed = 0

        r = requests.get("https://www.aljazeera.com/search/{}?page={}".format(keyword, page).replace(" ", "%20"))        
        soup = BeautifulSoup(r.content, "html.parser")

        #Handles cases where there are no articles on page 
        try:
            article_containers = soup.find_all("article")
        except:
            article_containers = []

        for i in article_containers:
            if ("2020" in i.text):
                url = [i.find("a").get("href"), "Al Jazeera", keyword, "aljazeera.com"]
                if url not in urls:
                    changed = 1
                    urls.append(url)

    #############################################################################################
    #                                  BBC                                                      #
    #############################################################################################
    print("Scanning BBC for {}".format(keyword))

    page = 0
    changed = 1
    while (changed):
        page += 1
        changed = 0

        r = requests.get("https://www.bbc.co.uk/search?q={}&page={}".format(keyword, page).replace(" ", "%20"))      
        soup = BeautifulSoup(r.content, "html.parser")

        #Handles cases where there are no articles on page 
        try:
            article_containers = soup.find("ul", {"class": "css-1lb37cz-Stack e1y4nx260"}).find_all("li")
        except:
            article_containers = []

        for i in article_containers:
            if ("2020" in i.text):
                date = i.find("span", {"class": "css-1hizfh0-MetadataSnippet ecn1o5v0"}).find("span", {"aria-hidden": "false"}).get_text()
                
                #Since in article if it is recent it will say "2 days ago" instead of the date, so I pass the date from search page to article scrapper
                url_text = "{}*{}".format(i.find("a").get("href"), date)
                if (not "news" in url_text or "newsround" in url_text):
                    continue
                url = [url_text, "British Broadcasting Company", keyword, "bbc.co.uk"]
                if url not in urls:
                    changed = 1
                    urls.append(url)
    
    #############################################################################################
    #                                 France 24                                                 #
    #   Notes:  This new site does not have search, Instead I used the corona virus, climate,   #
    #            and war tags                                                                   #
    #############################################################################################
    print("Scanning France24 for {}".format(keyword))

    web_address = ""
    page = 0
    changed = 1
    while (changed):
        page += 1
        changed = 0

        if (keyword == "Climate Change"):
            if (page > 1):
                web_address = "https://www.france24.com/en/tag/climate/{}/".format(page)
            else:
                web_address = "https://www.france24.com/en/tag/climate/"
        elif (keyword == "COVID 19"):
            if (page > 1):
                web_address = "https://www.france24.com/en/tag/coronavirus/{}/".format(page)
            else:
                web_address = "https://www.france24.com/en/tag/coronavirus/"
        elif (keyword == "Military Ground Vehicles"):
            if (page > 1):
                web_address = "https://www.france24.com/en/tag/war/{}/".format(page)
            else:
                web_address = "https://www.france24.com/en/tag/war/"

        print(web_address)

        r = requests.get(web_address, headers={'User-Agent': 'Mozilla/5.0'})
        soup = BeautifulSoup(r.content, "html.parser")
        #Handles cases where there are no articles on page 

        article_containers = soup.find_all("div", {"class": "m-item-list-article"})

        for i in article_containers:
            if ("2020" in i.text):
                url_text = "https://www.france24.com{}".format(i.find("a").get("href"))
                if "tv-shows" not in url_text and "video" not in url_text:
                    urls.append([url_text, "France 24", keyword, "france24.com"])
                changed = 1


    #############################################################################################
    #                                 Times of India                                            #
    #   Notes:  Covid pages on this site are formated differently than regular searches         #
    #############################################################################################
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
    
    

read_articles(urls)



