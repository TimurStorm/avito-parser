import csv
import requests
import csv
import vk_api
import random
import eel
from time import sleep
from bs4 import BeautifulSoup
from datetime import datetime
from .settings import DIR_PATH, VK


class Avito_parser:
    def __init__(self, pk, title, url, it, status="not active"):
        self.id = int(pk)
        self.title = title.strip()  # название
        self.url = url  # ссылка
        self.ads = []   # объявления
        self.ex = status.strip()  # параметр выхода из потока
        self.time = int(it)   # время итерации в минутах
        self.ads_file = DIR_PATH + "\\csv\\" + self.title + "_ads.csv"  # файл для хранения данных

    def create_ads_file(self):
        with open(self.ads_file, "w") as file:
            first_ads = []
            self.find_new_ads(url=self.url, ads_title=self.ads, ads_file=self.ads_file, mode=False)

    def write_parser(self):
        with open('csv/parsers.csv', 'a', encoding="utf-8") as file:
            writer = csv.writer(file, delimiter=",")
            writer.writerow([self.id, self.title, self.url, self.time, self.ex])

    def __str__(self):
        return "Парсер "+self.title

    # функция отправки сообщения
    def send_message(self, text):
        VK.messages.send(
            user_id=443194153,
            message=text,
            random_id=random.randint(-2147483648, +2147483647),
        )

    # находит объявления на сайте
    def get_all_ads(self, url):
        page = requests.get(url)
        print(page)
        code_dict = str(page)
        code = ""
        for i in code_dict:
            if i.isdigit():
                code += i
        resp = datetime.now().strftime("%d %B, %H:%M") + ": " + "Response code " + code
        soup = BeautifulSoup(page.content, "lxml")
        cont = soup.find("div", attrs={"data-marker": "catalog-serp"})
        ad = cont.find_all("div", attrs={"data-marker": "item"})
        return ad, resp

    # проверяет список объявлений на наличие новых предложений и в случае обнаружения присылает уведомление в лс в вк
    def find_new_ads(self, url, ads_title, ads_file, mode=True):
        with open(ads_file, encoding="utf-8") as file:
            reader = csv.reader(file, delimiter=",")
            for row in reader:
                ads_title.append(row[0])
        new_ad, resp = self.get_all_ads(url=url)
        for ad in new_ad:
            # ищем информацию о каждом объявлении
            info = ad.find("div", attrs={"class": "iva-item-body-NPl6W"})
            title_link = info.find(
                "div", attrs={"class": "iva-item-titleStep-2bjuh"}
            ).find("a", attrs={"data-marker": "item-title"})
            title = title_link.find("h3").get_text()
            new = Ad(title, url, 1)

            # если объявления нет в списке
            if new.title not in ads_title:
                link = "https://www.avito.ru" + title_link.get("href")
                if mode:
                    self.send_message(text="New Book!" + "\n" + title + "\n" + link)
                    ads_title.append(new)
                    eel.print("New Book!" + "\n" + title + "\n" + link)

                # записываем в файл новое объявление
                with open(ads_file, mode="a", encoding="utf-8") as file:
                    writer = csv.DictWriter(
                        file,
                        delimiter=",",
                        lineterminator="\r",
                        fieldnames=["Title", "Link"],
                    )
                    writer.writerow({"Title": title, "Link": link})
                sleep(2)
        eel.print(resp)


class Ad:
    def __init__(self, title, url, price):
        self.title = title
        self.price = price
        self.url = url
