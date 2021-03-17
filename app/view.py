import asyncio
import aiohttp
import eel
from bs4 import BeautifulSoup
from app.models import Avito_parser
from time import time


async def get(parser: Avito_parser):
    eel.print(f"Start work of {parser.title} parser")
    async with aiohttp.ClientSession() as session:
        while True:
            async with session.get(parser.url) as response:
                start_time = time()
                page = await response.text()
                # получаем код ответа
                resp = str(response.status)
                if resp == '200':
                    eel.print(f'Status code {resp}: Everything is okay')
                else:
                    eel.print(f'Nonamed code: {resp}')
                # начальная фильтрация контента
                soup = BeautifulSoup(page, "lxml")
                all_ads = soup.find("div", attrs={"data-marker": "catalog-serp"})
                """count = (
                    soup.find("span", attrs={"data-marker": "page-title/count"})
                    .get_text()
                    .replace(u"\xa0", "")
                    .replace(u"\u2009", "")
                )
                count = int(count.strip())  # общее количество объявлений"""
                ads = all_ads.find_all(
                    "div", attrs={"data-marker": "item"}
                )  # все сведения об объявлениях

                # переходим в обработчик новых объявлений
                parser.find_new_ads(new_ad=ads)
                print(f'====={parser.title}=====')
                print(f'====={round(time() - start_time,3)}=====')
                await asyncio.sleep(parser.time * 60.0)
