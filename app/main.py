import eel
import csv
import asyncio
from app.settings import WIND_SIZE, DIR_PATH, ACTIVE_PARSERS, MAIN_LOOP, API_ID
from app.models import Avito_parser
from app.view import wait_new_parser, parser_work
from auth.vk import VKAuth

with open(DIR_PATH + "\\csv\\parsers.csv", "r", encoding="utf-8") as file:
    reader = csv.reader(file, delimiter=",")
    for row in reader:
        if row != []:
            ACTIVE_PARSERS.append(Avito_parser(*row))

eel.init(DIR_PATH + "\\templates")
eel.print('000168154Tim', 'xbox')
eel.print('noobofmylive@gmail.com', 'xbox')

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
    Реадизовать методы на получение пароля, почты и одноразового кода "000168154Tim" "noobofmylive@gmail.com"
    """
    ep = eel.vk_auth_get_ep()()
    eel.vk_auth_set_ep_null()
    session = VKAuth(['friends'], API_ID, '11.9.1', pswd=ep[1], email=ep[0])
    session.auth()

    access_token = session.get_token()
    eel.set_auth_proc_false()
    print(access_token)


# close_callback - функция для закрытия приложения
eel.start("test.html", size=WIND_SIZE, port=5000)
# вставить сюда все то , что нужно вывести, главный поток
