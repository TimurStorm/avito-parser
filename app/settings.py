import asyncio
import os
import sqlite3
from pathlib import Path
from getpass import getuser

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


CONN = sqlite3.connect("../data/database.db")
CURSOR = CONN.cursor()
CURSOR.execute("""CREATE TABLE IF NOT EXISTS settings (title, value)""")

# если нет таблицы с настройками, то создаёт её и задаёт наальные настройки
if settings_not_exist(CURSOR):
    sqlite_insert_query = """INSERT INTO settings (title, value) VALUES (?, ?);"""
    default = [("window_size", "800, 600"), ("api_id", "7802615"), ("username", getuser())]

    CURSOR.executemany(sqlite_insert_query, default)
    CONN.commit()

CURSOR.execute(
    """CREATE TABLE IF NOT EXISTS parsers (name, url , timer, count, status, mailing, creation_date, update_date)"""
)

CURSOR.execute("""SELECT * from settings""")
settings = dict(CURSOR.fetchall())

WIND_SIZE = tuple([int(i) for i in settings["window_size"].split(", ")])

API_ID = settings["api_id"]

USERNAME = settings["username"]

ACTIVE_PARSERS = {}
TASKS = []

MAIN_LOOP = asyncio.get_event_loop()
