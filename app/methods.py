import eel
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from time import time as tm

from models import AvitoParser
from settings import *

"""
Файл для основных методов
"""


# отпралвяет запрос, получает html ответ, проводит первичную фильтрацию информации
def get_page(parser: AvitoParser, mode=True):
    start_time = tm()
    try:

        response = requests.get(parser.url)
        page_info = response.text
        # получаем код ответа
        status_code = str(response.status_code)

        # начальная фильтрация контента
        soup = BeautifulSoup(page_info, "lxml")
        all_ads = soup.find("div", attrs={"data-marker": "catalog-serp"})

        # все сведения об объявлениях
        ads = all_ads.find_all("div", attrs={"data-marker": "item"})

        # переходим в обработчик новых объявлений
        ads_new = parser.find_new_ads(new_ad=ads, mode=mode)

        # записываем изменения в базу данных
        CURSOR.executemany(
            f"INSERT INTO '{parser.title}' VALUES (?,?,?,?)", ads_new
        )
        info = (datetime.now().strftime("%d %B %H:%M:%S"), parser.title)
        sql = f"""UPDATE parsers SET update_date = ? WHERE name = ?"""
        CURSOR.execute(sql, info)
        CONN.commit()
        # Сохраняем изменения
        CONN.commit()
    except AttributeError:
        status_code = 400

    print(f"====={parser.title}=====")
    print(f"Status code: {status_code}")
    print(f"Time spent: {round(tm() - start_time, 3)} sec")
    if status_code != 400:
        print(f"Ads found: {len(ads)} ads")


@eel.expose
def create_parser(title, url, time):
    try:
        # создание объекта парсера
        new = AvitoParser(
            title=title,
            url=url,
            it=time,
            creation_date=datetime.now().strftime("%d %B %H:%M:%S"),
        )
        # Вставляем данные парсера в таблицу
        CURSOR.execute(
            f"""INSERT INTO 'parsers' VALUES ('{new.title}', '{new.url}', '{new.time}', '{new.count}','{new.status}',
            '{new.mailing}','{new.creation_date}', '{new.update_date}')"""
        )
        # Сохраняем изменения
        CONN.commit()
        # создаём таблицу для парсера
        CURSOR.execute(
            f"""CREATE TABLE IF NOT EXISTS '{new.title}' ('name', 'url' , 'price', 'see')"""
        )
        ALL_PARSERS[new.title] = new
        parser_work(parser=new)
        return True
    except Exception as e:
        return False


# включает парсер и одновляет таблицу бд
def parser_work(parser):
    # считываем уже имеющиеся объявления
    CURSOR.execute(f"""SELECT url from {parser.title}""")
    ads = CURSOR.fetchall()
    for url in ads:
        url = url[0]
        parser.ads.append(url)

    # запускаем основной цикл поиска ( с оповещениями)
    while parser.status == 'active':
        get_page(parser)
        eel.sleep(parser.time*60)
