class Avito_parser:
    def __init__(self, title, url, it):
        self.title = title  # название
        self.url = url  # ссылка
        self.ads = []   # объявления
        self.ex = "active"  # параметр выхода из потока
        self.time = it    # время итерации в минутах


class Ad:
    def __init__(self, title, url, price):
        self.title = title
        self.price = price
        self.url = url
