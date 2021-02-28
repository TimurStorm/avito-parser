import eel
from view import find_new_ads
from settings import *

eel.init("templates")

eel.start("main.html", block=False, size=WIND_SIZE)

# вставить сюда все то , что нужно вывести
while True:
    resp = find_new_ads()
    print(resp)
    if isinstance(resp, list):
        eel.addText(resp[0])
        if len(resp) == 2:
            eel.addText(resp[1])
    else:
        eel.addText(resp)
    eel.sleep(ITER_TIME * 60.0)