import eel
import asyncio
import vk_api
from app.settings import WIND_SIZE, DIR_PATH, ACTIVE_PARSERS, MAIN_LOOP, API_ID, CURSOR
from app.models import Avito_parser
from app.view import wait_new_parser, parser_work
from auth.vk import VKAuth

CURSOR.execute("""CREATE TABLE IF NOT EXISTS parsers (name, url , timer, count, status)""")

CURSOR.execute("""SELECT * from parsers""")
parsers = CURSOR.fetchall()
for parser in parsers:
    parser = list(parser)
    if parser[4] == "active":
        ACTIVE_PARSERS.append(Avito_parser(*parser))

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
    Реадизовать методы на получение пароля, почты и одноразового кода "000168154Tim" "noobofmylive@gmail.com"
    """
    ep = eel.vk_auth_get_ep()()
    eel.vk_auth_set_ep_null()
    session = VKAuth(["friends"], API_ID, "11.9.1", pswd=ep[1], email=ep[0])
    session.auth()

    access_token = session.get_token()
    session = vk_api.VkApi(token=access_token)
    VK = session.get_api()
    info = VK.account.getProfileInfo()
    eel.print(f"{info}", "xbox")


# close_callback - функция для закрытия приложения
eel.start("test.html", size=WIND_SIZE, port=5000)
# вставить сюда все то , что нужно вывести, главный поток
