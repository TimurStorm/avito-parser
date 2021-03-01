class Ad:
    def __init__(self, title, price, url, desc):
        self.title = title
        self.price = price
        self.url = url
        self.desc = desc


class New_avito_parser:
    def __init__(self, title, url, iter):
        self.title = title
        self.url = url
        self.iter = iter
        self.dict = []
