import eel
import requests
from time import ctime, strftime, strptime
from pprint import pprint
import settings

"""
Файл для вывода информациии на фронт
"""


def set_get():
    @eel.expose
    def get_parser_ads():

        resp = []
        for parser in settings.WORKING_PARSERS:
            ads = parser.ads
            info = [[ad.title, ad.price, parser.title, ad.pk] for ad in ads]
            resp += info
        return resp

    @eel.expose
    def get_all_parsers():
        info = [{"title": parser.title, "count": len(parser.ads), } for parser in settings.ALL_PARSERS]
        return info

    @eel.expose
    def get_all_settings():
        settings.CURSOR.execute("""SELECT * from settings""")
        sett = dict(settings.CURSOR.fetchall())
        return sett

    @eel.expose
    def get_ad_info(pk, parser: str):

        months = ['Января', 'Февраля', 'Марта', "Апреля", "Мая", "Июня",
                  "Июля", "Августа", "Сентября", "Октября", "Ноября", "Декабря"]

        try:
            params = {
                "key": 'af0deccbgcgidddjgnvljitntccdduijhdinfgjgfjir',
            }
            url_more_data_2 = 'https://m.avito.ru/api/15/items/' + str(pk)
            ad_data = requests.get(url_more_data_2, params=params).json()

            pprint(ad_data)

            date = ctime(ad_data['time'])
            date = strftime('%d %m %H:%M', strptime(date, '%a %b %d  %H:%M:%S %Y')).split()
            date[1] = months[int(date[1])-1]
            date = ' '.join(date)

            url = ad_data['seo']['canonicalUrl']

            params = ad_data['parameters']['flat']

            return {'img': ad_data['images'],
                    'desc': ad_data['description'],
                    'title': ad_data['title'],
                    'price': ad_data['price'],
                    'address': ad_data['address'],
                    'date': date,
                    'params': params,
                    'url': url}
        except Exception as e:
            print(e)
