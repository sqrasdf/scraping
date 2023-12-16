from bs4 import BeautifulSoup
import requests
import time

import http.client, urllib

api_token = "as7kmkwzoaxu7bzwdz6rjycp25rm2a"  # app token
user_key = "u759ikjxp3m64f91oudv2gd95u4b7v"   # my token
adik_key = "ufs46mazffpk9roie9kxhwwe81785o"   # adik's token


def notifySqr(message):
  conn = http.client.HTTPSConnection("api.pushover.net:443")
  conn.request("POST", "/1/messages.json",
    urllib.parse.urlencode({
      "token": api_token,
      "user": user_key,
      "message": message,
    }), { "Content-type": "application/x-www-form-urlencoded" })
  conn.getresponse()

def notifyAdik(message):
  conn = http.client.HTTPSConnection("api.pushover.net:443")
  conn.request("POST", "/1/messages.json",
    urllib.parse.urlencode({
      "token": api_token,
      "user": adik_key,
      "message": message,
    }), { "Content-type": "application/x-www-form-urlencoded" })
  conn.getresponse()


ids = []

link = "https://www.olx.pl/dla-dzieci/zabawki/klocki/q-lego-4195/?search%5Border%5D=created_at:desc"
offers_ids_list = []


def get_offers_quiet(link, offers_ids_list):
    html_text = requests.get(link).text
    soup = BeautifulSoup(html_text, "lxml")

    offers = soup.find("div", class_='css-oukcj3').find_all("div", class_="css-1sw7q4x")

    for offer in offers:
        id = offer.get("id")
        offers_ids_list.append(id)
    return offers_ids_list


def get_offers(link, offers_ids_list):
    html_text = requests.get(link).text
    soup = BeautifulSoup(html_text, "lxml")

    offers = soup.find("div", class_='css-oukcj3').find_all("div", class_="css-1sw7q4x")

    old_offers = offers_ids_list.copy()
    offers_ids_list = []

    for offer in offers:
        offer_name = offer.find("h6", class_ = "css-16v5mdi er34gjf0").text
        link = offer.find("a").get("href")
        link = "https://www.olx.pl" + link
        id = offer.get("id")

        if id not in old_offers:
            print("notifying about: " + offer_name + " " + id)
            notifySqr(offer_name + "\n" + link)
        offers_ids_list.append(id)
    return offers_ids_list


get_offers_quiet(link, offers_ids_list)

for item in offers_ids_list:
    print(item)

notifySqr("test first run")

while True:
    time.sleep(10)
    get_offers(link, offers_ids_list)


