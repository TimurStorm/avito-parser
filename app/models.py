import requests
import csv
import random
import eel
from time import time, sleep
from bs4 import BeautifulSoup
from datetime import datetime
from .settings import DIR_PATH, VK


class Avito_parser:
    def __init__(self, pk, title, url, it, status="not active"):
        self.id = int(pk)
        self.title = title.strip()  # название
        self.url = url  # ссылка
        self.ads = []  # объявления
        self.ex = status.strip()  # параметр выхода из потока
        self.time = int(it)  # время итерации в минутах
        self.ads_file = (
            DIR_PATH + "\\csv\\" + self.title + "_ads.csv"
        )  # файл для хранения данных

    def create_ads_file(self):
        with open(self.ads_file, "w"):
            self.find_new_ads(mode=False)

    def write_parser(self):
        with open("../csv/parsers.csv", "a", encoding="utf-8") as file:
            writer = csv.writer(file, delimiter=",")
            writer.writerow([self.id, self.title, self.url, self.time, self.ex])

    def __str__(self):
        return "Парсер " + self.title

    # функция отправки сообщения
    def send_message(self, text):
        VK.messages.send(
            user_id=443194153,
            message=text,
            random_id=random.randint(-2147483648, +2147483647),
        )
        sleep(0.5)

    # находит объявления на сайте
    def get_all_ads(self, url):
        start_time = time()
        page = requests.get(url)
        code_dict = str(page)
        code = ""
        print(f'Get html: {time() - start_time}')
        start_time = time()
        for i in code_dict:
            if i.isdigit():
                code += i
        print(f'Code to int: {time() - start_time}')
        start_time = time()
        resp = (
            self.title
            + " "
            + datetime.now().strftime("%d %B, %H:%M")
            + ": "
            + "Response code "
            + code
        )

        soup = BeautifulSoup(page.content, "lxml")

        all_ads = soup.find("div", attrs={"data-marker": "catalog-serp"})
        count = soup.find('span', attrs={"data-marker": "page-title/count"}).get_text().replace(u'\xa0','').replace(u'\u2009', '')
        count = int(count.strip())
        print(f"Количество объявлений {count}")
        ad = all_ads.find_all("div", attrs={"data-marker": "item"})
        print(f'Soup: {time() - start_time}')
        return ad, resp, count

    # проверяет список объявлений на наличие новых предложений и в случае обнаружения присылает уведомление в лс в вк
    def find_new_ads(self, mode=True):
        print("----------" + self.title + "----------")
        ads_file = self.ads_file
        url = self.url
        ads_title = self.ads
        with open(ads_file, encoding="utf-8") as file:
            reader = csv.reader(file, delimiter=",")
            for row in reader:
                ads_title.append(row[0])
        start_time = time()
        new_ad, resp, count = self.get_all_ads(url=url)
        if count - len(ads_title) > 0:
            print(f'{count - len(ads_title)} Новых объявлений!')
        print(f"Get uls {time() - start_time}")
        start_time = time()
        with open(ads_file, mode="a", encoding="utf-8") as file:
            writer = csv.writer(
                file,
                delimiter=",",
                lineterminator="\r",
            )

            for ad in new_ad:
                # ищем информацию о каждом объявлении
                info = ad.find("div", attrs={"class": "iva-item-body-NPl6W"})
                print(f"Find info about new ad: {time() - start_time}")
                start_time = time()
                title_link = info.find("a", attrs={"data-marker": "item-title"})
                print(f"Find title-link about new ad: {time() - start_time}")
                start_time = time()
                title = title_link.find("h3").get_text()
                print(f"Find title about new ad: {time() - start_time}")
                start_time = time()
                new = Ad(title, url, 1)

                # если объявления нет в списке
                if new.title not in ads_title:
                    link = "https://www.avito.ru" + title_link.get("href")
                    ads_title.append(new)
                    # записываем в файл новое объявление
                    writer.writerow([new.title, new.url])
                    if mode:
                        # присылает уведомление в ВК
                        self.send_message(text="New Book!" + "\n" + title + "\n" + link)
                        # выводит уведомление в приложении
                        eel.print("New Ad!" + "\n" + title + "\n" + link)

            eel.print(resp)


class Ad:
    def __init__(self, title, url, price):
        self.title = title
        self.price = price
        self.url = url
