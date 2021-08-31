import os
import sqlite3
from pathlib import Path
from getpass import getuser


"""
Файл для настроек
"""

DIR_PATH = str(Path(os.getcwd()))


# проверка на наличие настроек
def settings_not_exist(CURSOR):
    CURSOR.execute("""SELECT * from settings""")
    s = CURSOR.fetchall()
    if len(s) == 0:
        return True
    return False


# подключение к базе данных
CONN = sqlite3.connect(database=DIR_PATH + "\\data\\database.db")
CURSOR = CONN.cursor()
CURSOR.execute("""CREATE TABLE IF NOT EXISTS settings (title, value)""")

# если нет таблицы с настройками, то создаёт её и задаёт начальные настройки
if settings_not_exist(CURSOR):
    sqlite_insert_query = """INSERT INTO settings (title, value) VALUES (?, ?);"""
    default_settings = [
        ("window_size", "1280, 720"),
        ("username", getuser()),
    ]

    CURSOR.executemany(sqlite_insert_query, default_settings)
    CONN.commit()

CURSOR.execute(
    """CREATE TABLE IF NOT EXISTS parsers (name, url , timer, count, status, mailing, creation_date, update_date)"""
)

# подгрузка настроек из базы данных
CURSOR.execute("""SELECT * from settings""")
sett = dict(CURSOR.fetchall())

WIND_SIZE = tuple([int(i) for i in sett["window_size"].split(", ")])

USERNAME = sett["username"]

ALL_PARSERS = {}
WORKING_PARSERS = []
