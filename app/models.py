import csv
import random
import eel
from app.settings import DIR_PATH, VK, ACTIVE_PARSERS


def send_message(text):
    VK.messages.send(
        user_id=443194153,
        message=text,
        random_id=random.randint(-2147483648, +2147483647),
    )


class Avito_parser:
    def __init__(self, pk, title, url, it, status="active"):
        self.id = int(pk)  # индекс
        self.title = title.strip()  # название
        self.url = url  # ссылка
        self.ads = []  # объявления
        self.status = status.strip()  # параметр выхода из потока
        self.time = int(it)  # время итерации в минутах
        self.ads_file = (
            DIR_PATH + "\\csv\\" + self.title + "_ads.csv"
        )  # файл для хранения данных

    def write_parser(self, mode=False):
        if mode:
            with open("../csv/parsers.csv", "w", encoding="utf-8") as file:
                writer = csv.writer(file, delimiter=",")
                writer.writerows(
                    [parser.id, parser.title, parser.url, parser.time, parser.status]
                    for parser in ACTIVE_PARSERS
                )
        else:
            with open("../csv/parsers.csv", "a", encoding="utf-8") as file:
                writer = csv.writer(file, delimiter=",")
                writer.writerow([self.id, self.title, self.url, self.time, self.status])

    def __str__(self):
        return "Парсер " + self.title

    # проверяет список объявлений на наличие новых предложений и в случае обнаружения присылает уведомление в лс в вк
    def find_new_ads(
        self,
        mode=True,
        new_ad=None,
    ):

        ads_file = self.ads_file
        ads_title = self.ads

        with open(ads_file, encoding="utf-8") as file:
            reader = csv.reader(file, delimiter=",")
            for row in reader:
                ads_title.append(row[1])
        with open(ads_file, mode="a", encoding="utf-8") as file:
            writer = csv.writer(
                file,
                delimiter=",",
                lineterminator="\r",
            )

            for ad in new_ad:
                # ищем информацию о каждом объявлении
                info = ad.find("div", attrs={"class": "iva-item-body-NPl6W"})
                title_link = info.find("a", attrs={"data-marker": "item-title"})
                title = title_link.find("h3").get_text()
                link = "https://www.avito.ru" + title_link.get("href")

                new = Ad(title, link, 1)

                # если объявления нет в списке
                if new.url not in ads_title:

                    ads_title.append(new.url)
                    # записываем в файл новое объявление
                    writer.writerow([new.title, new.url])
                    if mode:
                        # присылает уведомление в ВК
                        send_message(
                            text="Новое объявление!" + "\n" + title + "\n" + link
                        )

                        # выводит уведомление в приложении
                        eel.print(
                            "----------New Ad!" + "\n" + title + "\n" + link, self.title
                        )


class Ad:
    def __init__(self, title, url, price):
        self.title = title
        self.price = price
        self.url = url
