import asyncio
import os
import rsa
import vk_api
import sqlite3
from pathlib import Path

"""
Файл для настроек
"""

DIR_PATH = str(Path(os.getcwd()).parent)


def settings_not_exist(CURSOR):
    CURSOR.execute("""SELECT * from settings""")
    s = CURSOR.fetchall()
    if len(s) == 0:
        return True
    return False


def get_private_key():
    key = rsa.PrivateKey(1, 2, 3, 4, 5).load_pkcs1(
        open("../data/private.pem", "rb").read()
    )
    return key


def get_public_key():
    key = rsa.PublicKey(1, 2).load_pkcs1(open("../data/public.pem", "rb").read())
    return key


def create_private_public_key():
    (public, privat) = rsa.newkeys(1024)
    """message = "hello Bob!".encode("utf8")
    crypto = rsa.encrypt(message, pub)
    message = rsa.decrypt(crypto, private)"""
    with open("../data/private.pem", mode="wb") as file:
        file.write(privat.save_pkcs1("PEM"))

    with open("../data/public.pem", mode="wb") as file:
        file.write(public.save_pkcs1("PEM"))


def set_vk_session(token):
    session = vk_api.VkApi(token=token)
    return session.get_api()


CONN = sqlite3.connect("../data/database.db")
CURSOR = CONN.cursor()
CURSOR.execute("""CREATE TABLE IF NOT EXISTS settings (title, value)""")

# если нет таблицы с настройками, то создаёт её и задаёт наальные настройки
if settings_not_exist(CURSOR):
    sqlite_insert_query = """INSERT INTO settings (title, value) VALUES (?, ?);"""
    default = [("window_size", "800, 600"), ("vk_token", None), ("api_id", "7802615")]

    CURSOR.executemany(sqlite_insert_query, default)
    CONN.commit()

CURSOR.execute(
    """CREATE TABLE IF NOT EXISTS parsers (name, url , timer, count, status, mailing, creation_date, update_date)"""
)

# если нет файлов с ключами , то содаёт их и обнуляет все токены
if not os.path.exists("../data/private.pem") or not os.path.exists("../db/public.pem"):
    create_private_public_key()
    CURSOR.execute("""SELECT title from settings""")
    s = CURSOR.fetchall()
    print(s)
    titles = [key for key in s if "token" in key]
    for title in titles:
        tokens = (None, title)
        sql_update_query = f"""UPDATE settings SET value = ? WHERE title = ?"""
        CURSOR.execute(sql_update_query, tokens)
    CONN.commit()


CURSOR.execute("""SELECT * from settings""")
settings = dict(CURSOR.fetchall())

WIND_SIZE = tuple([int(i) for i in settings["window_size"].split(", ")])

PRIVATE = get_private_key()
PUBLIC = get_public_key()

API_ID = settings["api_id"]

try:
    VK_TOKEN = rsa.decrypt(settings["vk_token"], PRIVATE).decode("utf-8")
    VK_SESSION = set_vk_session(VK_TOKEN)
except Exception:
    VK_SESSION = None
    VK_TOKEN = None
    print('Не валидный токен')


ACTIVE_PARSERS = {}
TASKS = []

MAIN_LOOP = asyncio.get_event_loop()
