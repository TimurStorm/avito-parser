import eel
import requests
from datetime import datetime
from time import time as tm
from models import AvitoParser, Ad
from settings import *

"""
Файл для основных методов
"""


# отпралвяет запрос, получает html ответ, проводит первичную фильтрацию информации
def get_page(parser: AvitoParser, mode=True):
    start_time = tm()
    try:

        params = {
            'query': parser.title.replace(' ', '+'),
            'limit': 50,
            'display': 'list',
            'locationId': 650400,
            'searchRadius': 100,
            'lastStamp': 1610905380,
            'key': 'af0deccbgcgidddjgnvljitntccdduijhdinfgjgfjir',
        }

        resp = requests.get('https://m.avito.ru/api/9/items', params=params).json()
        items = resp['result']['items']
        ads_new = []
        pks = [ad.pk for ad in parser.ads]
        for item in items:
            value = item['value']
            if item['type'] != 'vip':
                if 'list' in value.keys():
                    value = value['list']
                pk = value['id']
                title = value['title']
                price = value['price']
                if pk not in pks:
                    print('Новое объявление!')
                    ads_new.append((title, pk, price))

        # записываем изменения в базу данных
        CURSOR.executemany(
            f"INSERT INTO '{parser.title}' VALUES (?,?,?)", ads_new
        )
        CONN.commit()
        info = (datetime.now().strftime("%d %B %H:%M:%S"), parser.title)
        sql = f"""UPDATE parsers SET update_date = ? WHERE name = ?"""
        CURSOR.execute(sql, info)
        CONN.commit()
        # Сохраняем изменения
        for info in ads_new:
            ad = Ad(*info)
            parser.ads.append(ad)
        print(f"====={parser.title}=====")
        print(f"Status code: {resp['status']}")
        print(f"Time spent: {round(tm() - start_time, 3)} sec")
    except Exception as e:
        print(e)


@eel.expose
def create_parser(title, location, time):
    try:
        # создание объекта парсера
        new = AvitoParser(
            title=title,
            it=time,
            location=location,
            creation_date=datetime.now().strftime("%d %B %H:%M:%S"),
        )
        # Вставляем данные парсера в таблицу
        CURSOR.execute(
            f"""INSERT INTO 'parsers' VALUES ('{new.title}','{new.location}', '{new.time}', '{new.count}','{new.status}',
            '{new.mailing}','{new.creation_date}', '{new.update_date}')"""
        )
        # Сохраняем изменения
        CONN.commit()
        # создаём таблицу для парсера
        CURSOR.execute(
            f"""CREATE TABLE IF NOT EXISTS '{new.title}' ('title', 'pk' , 'price')"""
        )
        ALL_PARSERS.append(new)

        WORKING_PARSERS.append(new)
        eel.spawn(parser_work, new)
        return True
    except Exception as e:
        print(e)
        return False


# включает парсер и одновляет таблицу бд
def parser_work(parser):
    # считываем уже имеющиеся объявления
    CURSOR.execute(f"""SELECT * from "{parser.title}" """)
    ads = CURSOR.fetchall()
    for pk in ads:
        ad = Ad(*pk)
        parser.ads.append(ad)
    # запускаем основной цикл поиска ( с оповещениями)
    while parser.status == 'active':
        get_page(parser)
        eel.sleep(parser.time * 60)
