import eel
import settings
import asyncio

from app.models import Avito_parser
from app.methods import wait_new_parser, parser_work

from front.auth import login, reg

from pprint import pprint

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
resp = login(email="noobofmylive@gmail.com", password="000168154Tim")
pprint(resp.content.decode())
eel.init(settings.DIR_PATH + "\\templates")


@eel.expose
def loop():
    settings.MAIN_LOOP.run_until_complete(asyncio.gather(*settings.TASKS))


# close_callback - функция для закрытия приложения
eel.start("test.html", size=settings.WIND_SIZE, port=5000)
# вставить сюда все то , что нужно вывести, главный поток
