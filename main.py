import eel
from view import find_new_ads
from settings import *

eel.init(DIR_PATH)
eel.start(DIR_PATH + "\main.html", geometry={'size': WIND_SIZE, 'position': WIND_SIZE})
