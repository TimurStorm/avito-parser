import eel
import csv
from time import time as tm
from app.settings import WIND_SIZE, DIR_PATH
from app.models import Avito_parser


def close_app():
    #start = tm()
    for parser in active_parsers:
        if parser.ex == "active":
            set_thread(parser.id)
    #print(f'Time for start {tm()-start}')
    #print("##########All parser is working!##########")


active_parsers = []
with open(DIR_PATH + "\\csv\\parsers.csv", "r", encoding="utf-8") as file:
    reader = csv.reader(file, delimiter=",")
    for row in reader:
        if row != []:
            active_parsers.append(Avito_parser(*row))
print(DIR_PATH + "\\templates")
eel.init(DIR_PATH + "\\templates")


@eel.expose
def get_parser(pk):
    if active_parsers[pk].ex == "active":
        return True
    else:
        return False


@eel.expose
def set_ex(pk):
    pars = active_parsers[pk]
    eel.print("End of thread work: " + pars.title)
    pars.ex = "not active"


@eel.expose
def set_thread(pk):
    pars = active_parsers[pk]
    eel.print("Beginning of thread work: " + pars.title)
    pars.ex = "active"

    def my_thread():
        while pars.ex != "not active":
            pars.find_new_ads()
            eel.sleep(pars.time * 60.0)

    eel.spawn(my_thread)


@eel.expose
def create_parser(title, url, time):
    try:
        start = tm()
        new = Avito_parser(
            title=title, url=url, it=time, pk=len(active_parsers), status="active"
        )  # создает парсер
        active_parsers.append(new)  # добавляет объект в массив активных парсеров
        new.write_parser()  # записывает параметры парсера в файл
        new.create_ads_file()  # создает файл для хранения
        set_thread(len(active_parsers) - 1)  # запускает парсер
        print(f"Parser was created {float(tm())-start}")
    except Exception as e:
        print(f"Ошибка:{e}")


@eel.expose
def delete_parser(parsers: list, pk: int):
    set_ex(pk=pk)
    parsers.pop(pk)
    with open("../csv/parsers.csv", "w", encoding="utf-8") as file:
        writer = csv.writer(file, delimiter=",")
        for pars in parsers:
            writer.writerow(pars.title, pars.url, pars.time)


@eel.expose
def get_parsers():
    for parser in active_parsers:
        eel.print(parser.title + " " + parser.ex)


# close_callback - функция для закрытия приложения
eel.start("test.html", size=WIND_SIZE, close_callback=close_app())
# вставить сюда все то , что нужно вывести, главный поток
