import eel
import asyncio
from keyring import get_password
import settings
from models import Avito_parser, User
from methods import parser_work
from auth import login
from get import set_get

"""
Файл для сборки
"""





def set_auth():
    pwd = get_password(service_name="Parser", username=f"{settings.USERNAME}_pwd")
    ema = get_password(service_name="Parser", username=f"{settings.USERNAME}_ema")

    if ema is not None and pwd is not None:
        try:
            resp = login(email=ema, password=pwd)
            info = resp["user"]
            USER = User(
                username=info["username"], email=info["email"], vk_id=info["vk_id"]
            )
            settings.USERNAME = USER.username
        except Exception:
            print("Ошибка авторизации")


def set_parsers():
    settings.CURSOR.execute("""SELECT * from parsers""")
    parsers = settings.CURSOR.fetchall()
    for parser in parsers:
        parser = list(parser)
        if parser[4] == "active":
            new = Avito_parser(*parser)
            settings.ACTIVE_PARSERS[parser[0]] = new
            settings.TASKS.append(parser_work(parser=new))


def main():
    set_auth()  # все auth-методы
    set_parsers()  # вся информация о парсерах
    set_get()  # все get-методы
    eel.init('client')

    # @eel.expose
    # def start_all_parsers():
    #     def started():
    #         if not settings.MAIN_LOOP.is_running():
    #             settings.MAIN_LOOP.run_until_complete(
    #                 asyncio.gather(*settings.TASKS)
    #             )
    #     eel.spawn(started)

    eel.start({
        'port': 3000
    }, options={
        'block': False,
        'size': settings.WIND_SIZE,
        'port': 8888,
        'host': 'localhost',
    }, suppress_error=True)
    while True:
        eel.sleep(1)


if __name__ == "__main__":
    main()
