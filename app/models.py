
"""
Файл для объявления моделей
"""


class AvitoParser:
    def __init__(
        self,
        title,
        url,
        it,
        count=1,
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
    def find_new_ads(
        self,
        mode=True,
        new_ad=None,
    ):

        ads_url = self.ads
        ads_new = []  # список новых объявлений

        for ad in new_ad:
            # ищем информацию о каждом объявлении
            title_link = ad.find("a", attrs={"data-marker": "item-title"})
            title = title_link.find("h3").get_text()
            link = "https://www.avito.ru" + title_link.get("href")
            price = (
                ad.find("span", attrs={"data-marker": "item-price"})
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

                # добавляем новое объявление будующей проверки
                ads_new.append((new.title, new.url, new.price, False))
                self.ads.append(new.url)

        return ads_new


class Ad:
    def __init__(self, title, url, price):
        self.title = title
        self.price = price
        self.url = url


class User:
    def __init__(self, username, email, vk_id):
        self.username = username
        self.email = email
        self.vk_id = vk_id


