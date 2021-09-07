import eel
import settings
from models import AvitoParser, User
from methods import parser_work
from auth import set_auth
from get import set_get

"""
Файл для сборки
"""


def set_parsers():
    settings.CURSOR.execute("""SELECT * from parsers""")
    parsers = settings.CURSOR.fetchall()
    for parser in parsers:
        parser = list(parser)
        if parser[4] == "active":
            new = AvitoParser(*parser)
            settings.ALL_PARSERS.append(new)


def main():
    set_auth()  # подключение auth-методов
    set_parsers()  # подгрузка информации о парсерах
    set_get()  # подключение get-методов
    eel.init('src')

    # функция включения парсеров
    @eel.expose
    def start_all_parsers():
        for parser in settings.ALL_PARSERS:
            if parser not in settings.WORKING_PARSERS:
                settings.WORKING_PARSERS.append(parser)
                eel.spawn(parser_work, parser)
        eel.set_js_parser()

    eel.start({
        'port': 3000
    }, options={
        'block': False,
        'time_shutdown': 600000,
        'size': settings.WIND_SIZE,
    }, suppress_error=True)
    while True:
        eel.sleep(1)


if __name__ == "__main__":
    main()
