import aiohttp
import eel
import csv
import asyncio
from bs4 import BeautifulSoup
from app.settings import WIND_SIZE, DIR_PATH, ACTIVE_PARSERS, MAIN_LOOP, API_ID, VK_FORM
from app.models import Avito_parser
from app.view import wait_new_parser, parser_work
from auth.vk import VKAuth

with open(DIR_PATH + "\\csv\\parsers.csv", "r", encoding="utf-8") as file:
    reader = csv.reader(file, delimiter=",")
    for row in reader:
        if row != []:
            ACTIVE_PARSERS.append(Avito_parser(*row))

eel.init(DIR_PATH + "\\templates")


@eel.expose
def loop():
    tasks = []

    for parser in ACTIVE_PARSERS:
        if parser.status == "active":
            tasks.append(parser_work(parser=parser))

    tasks.append(wait_new_parser())

    MAIN_LOOP.run_until_complete(asyncio.gather(*tasks))


@eel.expose
def vk_auth():
    """
    Реадизовать методы на получение пароля, почты и одноразового кода
    """
    session = VKAuth(['friends'], API_ID, '11.9.1', pswd="000168154Tim", email="noobofmylive@gmail.com")
    session.auth()

    access_token = session.get_token()
    print(access_token)


# close_callback - функция для закрытия приложения
eel.start("test.html", size=WIND_SIZE, port=5000)
# вставить сюда все то , что нужно вывести, главный поток
