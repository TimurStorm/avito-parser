import eel
import aiohttp

from bs4 import BeautifulSoup
from datetime import datetime
from time import time as tm

from models import Avito_parser
from settings import *

"""
Файл для основных методов
"""


async def parser_update(parser: Avito_parser):
    futures = []

    for i in range(parser.count):
        futures.append(
            MAIN_LOOP.create_task(get(parser=parser, cycle=False, mode=False, page=i))
        )
    await asyncio.gather(*futures)


# отпралвяет запрос, получает html ответ, проводит первичную фильтрацию информации
async def get(parser: Avito_parser, mode=True, cycle=True, page=1):
    async with aiohttp.ClientSession() as session:
        if not cycle:
            if "?" in parser.url:
                url = parser.url + "&p=" + str(page)
            else:
                url = parser.url + "?p=" + str(page)
        else:
            url = parser.url
        while parser.status == "active":
            async with session.get(url) as response:
                start_time = tm()
                page_info = await response.text()
                # получаем код ответа
                resp = str(response.status)

                # начальная фильтрация контента
                soup = BeautifulSoup(page_info, "lxml")
                all_ads = soup.find("div", attrs={"data-marker": "catalog-serp"})

                # все сведения об объявлениях
                ads = all_ads.find_all("div", attrs={"data-marker": "item"})

                # переходим в обработчик новых объявлений
                ads_new = await parser.find_new_ads(new_ad=ads, mode=mode)

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
                if not cycle:
                    break

                print(f"====={parser.title}=====")
                print(f"Time spent: {round(tm() - start_time, 3)} sec")
                print(f"Ads found: {len(ads)} ads")

            await asyncio.sleep(parser.time * 60.0)


@eel.expose
def create_parser(title, url, time):
    try:
        # создание объекта парсера
        new = Avito_parser(
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
        ACTIVE_PARSERS[new.title] = new
        MAIN_LOOP.create_task(parser_work(parser=new))
        return True
    except Exception as e:
        return False


# включает парсер и одновляет таблицу бд
async def parser_work(parser):
    # считываем уже имеющиеся объявления

    CURSOR.execute(f"""SELECT url from {parser.title}""")
    ads = CURSOR.fetchall()
    for url in ads:
        url = url[0]
        parser.ads.append(url)

    # запускаем обработчик новых объявлений( без оповещений)
    futures = []

    futures.append(MAIN_LOOP.create_task(parser_update(parser=parser)))
    await asyncio.gather(*futures)

    # запускаем основной цикл поиска ( с оповещениями)
    futures[0] = MAIN_LOOP.create_task(get(parser=parser))
    await asyncio.gather(*futures)


# остановка парсера
def parser_stop(parser_name: str):
    parser = ACTIVE_PARSERS[parser_name]
    parser.status = "not active"



