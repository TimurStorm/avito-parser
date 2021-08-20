import eel
import requests
from bs4 import BeautifulSoup

import settings

"""
Файл для вывода информациии на фронт
"""


def set_get():
    @eel.expose
    def get_parser_ads():

        # TODO: модифицировать до выдачи объектов Ad, избавиться от sql запроса

        resp = []
        parser_names = [parser.title for parser in settings.WORKING_PARSERS]
        try:
            for name in parser_names:
                settings.CURSOR.execute(f"""SELECT * from {name}""")
                info = settings.CURSOR.fetchall()
                info = [[i[0], i[2], name, i[1]] for i in info]
                resp += info
        except TypeError:
            pass
        return resp

    @eel.expose
    def get_all_parsers():
        settings.CURSOR.execute(f"""SELECT name, timer from parsers""")
        info = settings.CURSOR.fetchall()
        info = [[i[0] for i in info], [i[1] for i in info]]
        return info

    @eel.expose
    def get_all_settings():
        settings.CURSOR.execute("""SELECT * from settings""")
        sett = dict(settings.CURSOR.fetchall())
        return sett

    @eel.expose
    def get_ad_info(url: str, parser: str):
        response = requests.get(url)
        page_info = response.text

        settings.CURSOR.execute(f"""SELECT name, price from {parser} WHERE url='{url}'""")
        info = settings.CURSOR.fetchall()

        soup = BeautifulSoup(page_info, 'lxml')
        data = soup.find("div", attrs={"class": "item-view-content"})
        img = data.find_all('div', attrs={"class": "gallery-img-frame js-gallery-img-frame"})
        img = [i.get('data-url') for i in img]

        desc_p = data.find('div', attrs={"class": "item-description"}).find_all('p')
        desc = ''
        for p in desc_p:
            desc += p.get_text()

        return {'img': img,
                'desc': desc,
                'title': info[0][0],
                'price': info[0][1]
                }