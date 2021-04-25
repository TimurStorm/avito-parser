import eel
import rsa
import vk_api

import settings
import asyncio
from app.models import Avito_parser
from app.methods import wait_new_parser, parser_work
from auth.vk import VKAuth

"""
Файл для сборки
"""

settings.CURSOR.execute("""SELECT * from parsers""")
parsers = settings.CURSOR.fetchall()
# , mailing, creation_date, update_date)
for parser in parsers:
    parser = list(parser)
    if parser[4] == "active":
        new = Avito_parser(*parser)
        settings.ACTIVE_PARSERS[parser[0]] = new
        settings.TASKS.append(parser_work(parser=new))

settings.TASKS.append(wait_new_parser())
eel.init(settings.DIR_PATH + "\\templates")


@eel.expose
def loop():
    settings.MAIN_LOOP.run_until_complete(asyncio.gather(*settings.TASKS))


@eel.expose
def vk_auth():
    """
    Реадизовать методы на получение пароля, почты и одноразового кода "000168154Tim" "noobofmylive@gmail.com"
    """
    ep = eel.vk_auth_get_ep()()
    session = VKAuth(
        ["friends", "offline"], settings.API_ID, "11.9.1", pswd=ep[1], email=ep[0]
    )
    session.auth()

    access_token = session.get_token()
    eel.vk_auth_set_ep_null()

    settings.VK_TOKEN = access_token
    settings.VK_SESSION = settings.set_vk_session(settings.VK_TOKEN)

    info = (rsa.encrypt(access_token.encode("utf8"), settings.PUBLIC), "vk_token")
    sql = f"""UPDATE settings SET value = ? WHERE title = ?"""
    settings.CURSOR.execute(sql, info)
    settings.CONN.commit()

    session = vk_api.VkApi(token=access_token)
    VK = session.get_api()
    info = VK.account.getProfileInfo()
    eel.print(f"{info}", "xbox")


# close_callback - функция для закрытия приложения
eel.start("test.html", size=settings.WIND_SIZE, port=5000)
# вставить сюда все то , что нужно вывести, главный поток
