import eel
from app.view import find_new_ads
from app.settings import *

eel.init("templates")


# вторичный поток
"""
def my_other_thread():
    while True:
        print("I'm a thread")
        eel.sleep(1.0)


eel.spawn(my_other_thread)"""


@eel.expose
def tim():
    while True:
        resp = find_new_ads()
        eel.addText(resp)
        eel.sleep(60.0)

eel.start("main.html", size=WIND_SIZE)

# вставить сюда все то , что нужно вывести, главный поток
"""while True:
    eel.addText(find_new_ads())
    eel.sleep(30.0)
"""