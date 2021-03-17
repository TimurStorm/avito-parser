import eel
import csv
import asyncio
from app.settings import WIND_SIZE, DIR_PATH
from app.models import Avito_parser
from app.view import get

active_parsers = []
with open(DIR_PATH + "\\csv\\parsers.csv", "r", encoding="utf-8") as file:
    reader = csv.reader(file, delimiter=",")
    for row in reader:
        if row != []:
            active_parsers.append(Avito_parser(*row))
print(DIR_PATH + "\\templates")
eel.init(DIR_PATH + "\\templates")

"""
@eel.expose
def create_parser(title, url, time):
    try:
        start = tm()
        new = Avito_parser(
            title=title, url=url, it=time, pk=len(active_parsers), status="active"
        )  # создает парсер
        active_parsers.append(new)  # добавляет объект в массив активных парсеров
        new.write_parser()  # записывает параметры парсера в файл
        new.edit_or_create_ads_file()  # создает файл для хранения
        #set_thread(len(active_parsers) - 1)  # запускает парсер
        print(f"Parser was created {float(tm())-start}")
    except Exception as e:
        print(f"Ошибка:{e}")"""


tasks = [get(parser=active_parsers[0])]


@eel.expose
def loop():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.gather(*tasks))


# close_callback - функция для закрытия приложения
eel.start("test.html", size=WIND_SIZE)
# вставить сюда все то , что нужно вывести, главный поток
