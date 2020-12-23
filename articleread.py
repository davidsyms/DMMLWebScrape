from bs4 import BeautifulSoup
import requests

#open url and create soup
r = requests.get("https://ceasefiremagazine.co.uk/stay-home-save-lives-ask-questions-on-proportionality-during-this-crisis/")
soup = BeautifulSoup(r.content, "html.parser")

date_unstripped = soup.find("div", {"class": "column_main"}).find("i").get_text()
date_stripped = date_unstripped[14: date_unstripped[2:].find("-")+1]
print("\n\nDate: {}\n\n".format(date_stripped))

headline = soup.find("h1", {"itemprop": "name headline"}).get_text()
print("Headline: {}\n\n".format(headline))

textdiv = soup.find("div", {"id": "entry"})
for remove in textdiv.find_all("div"):
    remove.decompose()
text = textdiv.find_all("p")

author = text[0].get_text()[3:]
print("Author: {}\n\n".format(author))

article = ""
for i in text[1:]:
    article += i.get_text()
print(article)


print("\n\n")