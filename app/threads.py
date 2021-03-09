import csv
import eel
from .view import find_new_ads, write_parser
from .models import Avito_parser
from main import active_parsers


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
        while pars.ex is not "not active":
            find_new_ads(url=pars.url, ads_title=pars.ads)
            eel.sleep(pars.time * 60.0)

    eel.spawn(my_thread)


@eel.expose
def create_parser(title, url, time):
    new = Avito_parser(title=title, url=url, time=time)
    active_parsers.append(new)
    write_parser(new)
    set_thread(len(active_parsers)-1)


@eel.expose
def delete_writer(parsers: list, parser: Avito_parser):
    parsers.remove(parser)
    with open('csv/parsers.csv', 'w', encoding="utf-8") as file:
        writer = csv.writer(file, delimiter=",")
        for pars in parsers:
            writer.writerow(pars.title, pars.url, pars.time)