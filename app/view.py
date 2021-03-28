from datetime import datetime

from app.models import *
import os
import eel
import asyncio
import aiohttp
from bs4 import BeautifulSoup
from time import time as tm
from app.settings import ACTIVE_PARSERS, CURSOR
from app.settings import MAIN_LOOP


async def edit_or_create_ads_file(parser: Avito_parser, page_count=5):
    if os.path.exists(parser.ads_file):
        mode = "a"
    else:
        mode = "w"
    with open(parser.ads_file, mode):
        futures = []

        for i in range(page_count):
            futures.append(
                MAIN_LOOP.create_task(
                    get(parser=parser, cycle=False, mode=False, page=i)
                )
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
            eel.print(f"Start work of {parser.title} parser", parser.title)
            url = parser.url
        while parser.status == "active":
            try:
                async with session.get(url) as response:
                    start_time = tm()
                    page_info = await response.text()
                    # получаем код ответа
                    resp = str(response.status)
                    if cycle:
                        if resp == "200":
                            eel.print(
                                f"{datetime.now().strftime('%d %B %H:%M:%S')} parser {parser.title} Status code {resp}: Everything is okay",
                                parser.title,
                            )
                        else:
                            eel.print(
                                f"{datetime.now().strftime('%d %B %H:%M:%S')} parser {parser.title} Nonamed code: {resp}",
                                parser.title,
                            )
                    # начальная фильтрация контента
                    soup = BeautifulSoup(page_info, "lxml")
                    all_ads = soup.find("div", attrs={"data-marker": "catalog-serp"})
                    """count = (
                        soup.find("span", attrs={"data-marker": "page-title/count"})
                        .get_text()
                        .replace("\xa0", "")
                        .replace("\u2009", "")
                    )
                    count = int(count.strip())  # общее количество объявлений"""
                    ads = all_ads.find_all(
                        "div", attrs={"data-marker": "item"}
                    )  # все сведения об объявлениях
                    # переходим в обработчик новых объявлений
                    parser.find_new_ads(new_ad=ads, mode=mode)
                    if not cycle:
                        eel.print(
                            f"--Page: {page} Time spent: {round(tm() - start_time,4)} sec. Ads count: {len(ads)}",
                            parser.title,
                        )
                        break
                    print(f"====={parser.title}=====")
                    print(f"Time spent: {round(tm() - start_time,3)} sec", parser.title)
                    print(f"Ads found: {len(ads)} ads", parser.title)
            except Exception as e:
                print(f"ERROR: {e}", parser.title)
                eel.print(f"ERROR: {e}", parser.title)
            await asyncio.sleep(parser.time * 60.0)


# ожидает создание нового парсера
async def wait_new_parser():
    while True:
        resp = eel.wait_new_parser_js()()
        if type(resp) is list:
            print()
            if resp[2].isdigit and resp[3].isdigit:
                start_time = tm()
                # создание парсера
                new = Avito_parser(
                    pk=len(ACTIVE_PARSERS), title=resp[0], url=resp[1], it=resp[2]
                )
                # добавление парсера в список активных
                new.write_parser()
                #CURSOR.execute(f"""CREATE TABLE {new.title} (title, url, time, status) """)
                ACTIVE_PARSERS.append(new)
                eel.print("Create new parser")
                futures = [
                    MAIN_LOOP.create_task(
                        edit_or_create_ads_file(parser=new, page_count=int(resp[3]))
                    )
                ]
                await asyncio.gather(*futures)
                eel.all_is_none()
                eel.print(f"Parser was created for {round(tm() - start_time,4)}")
                asyncio.create_task(get(parser=new))
        await asyncio.sleep(1)


async def parser_work(parser):
    futures = []
    eel.print("Information update:", parser.title)
    eel.print("====================", parser.title)
    futures.append(MAIN_LOOP.create_task(edit_or_create_ads_file(parser=parser)))
    await asyncio.gather(*futures)
    eel.print("====================", parser.title)
    futures[0] = MAIN_LOOP.create_task(get(parser=parser))
    await asyncio.gather(*futures)


def parser_stop(parser_id: Avito_parser):
    parser = ACTIVE_PARSERS[parser_id]
    parser.status = "not active"
    parser.write_parser(mode=True)