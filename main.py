import eel
import csv
from app.settings import WIND_SIZE, ITER_TIME
from app.view import find_new_ads
from app.models import Avito_parser

active_parsers = []
with open('parsers.csv', 'r', encoding="utf-8") as file:
    reader = csv.reader(file, delimiter=",")
    for row in reader:
        active_parsers.append(Avito_parser(*row))

eel.init("templates")


@eel.expose
def set_id(pk):
    pars = active_parsers[pk]
    eel.addText("End of thread work: " + pars.title)
    pars.id = "active"


@eel.expose
def set_thread(pk):
    pars = active_parsers[pk]
    eel.addText("Beginning of thread work: " + pars.title)
    pars.id = None

    def my_thread():
        while pars.id is None:
            find_new_ads(url=pars.url, ads_title=pars.ads)
            eel.sleep(pars.it * 60.0)

    eel.spawn(my_thread)


eel.start("main.html", size=WIND_SIZE)
# вставить сюда все то , что нужно вывести, главный поток
