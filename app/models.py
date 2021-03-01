class Avito_parser:
    def __init__(self, title, url, it):
        self.title = title  # название
        self.url = url  # ссылка
        self.ads = []   # объявления
        self.id = None  # параметр выхода из потока
        self.it = it