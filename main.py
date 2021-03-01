import eel
from app.view import find_new_ads
from app.settings import *

eel.init("templates")


def my_other_thread():
    while True:
        eel.test()
        eel.sleep(ITER_TIME * 60.0)


eel.spawn(my_other_thread)


eel.start("main.html", size=WIND_SIZE)

# вставить сюда все то , что нужно вывести, главный поток
while True:
   pass
