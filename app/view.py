import requests
import csv
import vk_api
import random
import eel
from .settings import *
from time import sleep
from bs4 import BeautifulSoup
from datetime import datetime

token = "56036fde45f5c4e10920de4ad5d1b7c6bf4f78feb37395313eec5fa2acf991d43a7f2ae5ca0f4f9688213"
session = vk_api.VkApi("89172461399", "000168154Tim", token=token)
vk = session.get_api()


# функция отправки сообщения
def send_message(text):
    vk.messages.send(
        user_id=443194153,
        message=text,
        random_id=random.randint(-2147483648, +2147483647),
    )


# находит объявления на сайте
def get_all_ads(url):
    page = requests.get(url)
    code_dict = str(page)
    code = ""
    for i in code_dict:
        if i.isdigit():
            code += i
    resp = datetime.now().strftime("%d %B, %H:%M") + ": " + "Response code " + code
    soup = BeautifulSoup(page.content, "lxml")
    # print(soup.prettify())
    cont = soup.find("div", attrs={"data-marker": "catalog-serp"})
    ad = cont.find_all("div", attrs={"data-marker": "item"})
    return ad, resp


# проверяет список объявлений на наличие новых предложений и в случае обнаружения присылает уведомление в лс в вк
def find_new_ads(url, ads_title):
    with open(DIR_PATH + "/csv/ads.csv", encoding="utf-8") as file:
        reader = csv.reader(file, delimiter=",")
        for row in reader:
            ads_title.append(row[0])
    new_ad, resp = get_all_ads(url=url)
    for ad in new_ad:
        # ищем информацию о каждом объявлении
        info = ad.find("div", attrs={"class": "iva-item-body-NPl6W"})
        title_link = info.find(
            "div", attrs={"class": "iva-item-titleStep-2bjuh"}
        ).find("a", attrs={"data-marker": "item-title"})
        title = title_link.find("h3").get_text()

        # если объявления нет в списке
        if title not in ads_title:
            link = "https://www.avito.ru" + title_link.get("href")
            send_message(text="New Book!" + "\n" + title + "\n" + link)
            ads_title.append(title)
            eel.addText("New Book!" + "\n" + title + "\n" + link)

            # записываем в файл новое объявление
            with open(DIR_PATH + "/csv/ads.csv", mode="a", encoding="utf-8") as file:
                writer = csv.DictWriter(
                    file,
                    delimiter=",",
                    lineterminator="\r",
                    fieldnames=["Title", "Link"],
                )
                writer.writerow({"Title": title, "Link": link})
            sleep(2)
    eel.addText(resp)