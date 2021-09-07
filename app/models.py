
"""
Файл для объявления моделей
"""


class AvitoParser:
    def __init__(
        self,
        title,
        location,
        it,
        count=1,
        status="active",
        mailing=None,
        creation_date=None,
        update_date=None,
    ):
        self.location = location
        self.update_date = update_date  # дата последнего обновления
        self.creation_date = creation_date  # дата создания
        self.title = title.strip()  # название
        self.count = int(count)
        self.ads = []  # объявления
        self.status = status.strip()  # параметр выхода из потока
        self.time = int(it)  # время итерации в минутах
        self.mailing = mailing  # дата рассылки

    def __str__(self):
        return self.title


class Ad:
    def __init__(self, title, pk, price):
        self.title = title
        self.pk = pk
        self.price = price


class User:
    def __init__(self, username, email, vk_id):
        self.username = username
        self.email = email
        self.vk_id = vk_id


