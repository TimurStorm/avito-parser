import eel
import csv
from app.settings import WIND_SIZE
from app.models import Avito_parser

active_parsers = []
with open('csv/parsers.csv', 'r', encoding="utf-8") as file:
    reader = csv.reader(file, delimiter=",")
    for row in reader:
        active_parsers.append(Avito_parser(*row))

eel.init("templates")

# close_callback - функция для закрытия приложения
eel.start("main.html", size=WIND_SIZE)
# вставить сюда все то , что нужно вывести, главный поток
