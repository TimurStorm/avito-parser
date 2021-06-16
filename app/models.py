import eel
import requests

"""
Файл для объявления моделей
"""


class Avito_parser:
    def __init__(
            self,
            title,
            url,
            it,
            count,
            status="active",
            mailing=None,
            creation_date=None,
            update_date=None,
    ):
        self.update_date = update_date  # дата последнего обновления
        self.creation_date = creation_date  # дата создания
        self.title = title.strip()  # название
        self.url = url  # ссылка
        self.count = int(count)
        self.ads = []  # объявления
        self.status = status.strip()  # параметр выхода из потока
        self.time = int(it)  # время итерации в минутах
        self.mailing = mailing  # дата рассылки

    def __str__(self):
        return self.title

    # проверяет список объявлений на наличие новых предложений и в случае обнаружения присылает уведомление в лс в вк
    async def find_new_ads(
            self,
            mode=True,
            new_ad=None,
    ):

        ads_url = self.ads
        ads_new = []  # список новых объявлений

        for ad in new_ad:
            # ищем информацию о каждом объявлении
            info = ad.find("div", attrs={"class": "iva-item-body-NPl6W"})
            title_link = info.find("a", attrs={"data-marker": "item-title"})
            title = title_link.find("h3").get_text()
            link = "https://www.avito.ru" + title_link.get("href")
            price = (
                info.find("span", attrs={"data-marker": "item-price"})
                    .find(
                    "span",
                    attrs={
                        "class": "price-text-1HrJ_ text-text-1PdBw text-size-s-1PUdo"
                    },
                )
                    .get_text()
            )

            # для удобства создаём новый объект класса Ad
            new = Ad(title, link, price)

            # если объявления нет в списке
            if new.url not in ads_url:

                # добавляем новое объявление в список для бд и будующей проверки
                ads_new.append((new.title, new.url, new.price, False))
                self.ads.append(new.url)

                if mode:
                    text = "----------New Ad!" + "\n" + title + "\n" + link
                    # присылает уведомление в ВК
                    requests.post(f'http://localhost:70/send/?pk=443194153&text={text}')

                    # выводит уведомление в приложении
                    eel.print(
                        text, self.title
                    )

        return ads_new


class Ad:
    def __init__(self, title, url, price):
        self.title = title
        self.price = price
        self.url = url

    def __str__(self):
        return f"Объявление: {self.title} по цене {self.price}"


class User:
    def __init__(self, username, vk_id, email):
        self.username = username
        self.email = email
        self.vk_id = vk_id
