import eel
import csv
import asyncio
from app.settings import WIND_SIZE, DIR_PATH, ACTIVE_PARSERS, MAIN_LOOP
from app.models import Avito_parser
from app.view import get, wait_new_parser

with open(DIR_PATH + "\\csv\\parsers.csv", "r", encoding="utf-8") as file:
    reader = csv.reader(file, delimiter=",")
    for row in reader:
        if row != []:
            ACTIVE_PARSERS.append(Avito_parser(*row))

eel.init(DIR_PATH + "\\templates")


@eel.expose
def loop():
    tasks = [get(parser=ACTIVE_PARSERS[i]) for i in range(len(ACTIVE_PARSERS))]

    tasks.append(wait_new_parser())

    MAIN_LOOP.run_until_complete(asyncio.gather(*tasks))


# close_callback - функция для закрытия приложения
eel.start("test.html", size=WIND_SIZE)
# вставить сюда все то , что нужно вывести, главный поток
