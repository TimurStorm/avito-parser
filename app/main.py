import eel
from keyring import get_password

import settings
import asyncio

from app.models import Avito_parser, User
from app.methods import parser_work
from front.auth import login

"""
Файл для сборки
"""

pwd = get_password(service_name="Parser", username=f"{settings.USERNAME}_pwd")
ema = get_password(service_name="Parser", username=f"{settings.USERNAME}_ema")

if ema is not None and pwd is not None:
    resp = login(email=ema, password=pwd)
    info = resp["user"]
    USER = User(username=info["username"], email=info["email"], vk_id=info["vk_id"])
    settings.USERNAME = USER.username

settings.CURSOR.execute("""SELECT * from parsers""")
parsers = settings.CURSOR.fetchall()
for parser in parsers:
    parser = list(parser)
    if parser[4] == "active":
        new = Avito_parser(*parser)
        settings.ACTIVE_PARSERS[parser[0]] = new
        settings.TASKS.append(parser_work(parser=new))

eel.init(settings.DIR_PATH + "\\templates")

eel.print(f"Привет {settings.USERNAME}", "xbox")


@eel.expose
def loop():
    settings.MAIN_LOOP.run_until_complete(asyncio.gather(*settings.TASKS))


# close_callback - функция для закрытия приложения
eel.start("test.html", size=settings.WIND_SIZE, port=5050)
# вставить сюда все то , что нужно вывести, главный поток
