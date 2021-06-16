import eel
from app.settings import CURSOR

"""
Файл для вывода информациии на фронт
"""


@eel.expose
def get_parser_ads(parser_name: str):
    CURSOR.execute(f"""SELECT * from '{parser_name}'""")
    info = dict(CURSOR.fetchall())
    return info


@eel.expose
def get_all_parsers():
    CURSOR.execute(f"""SELECT * from parsers""")
    info = dict(CURSOR.fetchall())
    return info


@eel.expose
def get_all_settings():
    CURSOR.execute("""SELECT * from settings""")
    settings = dict(CURSOR.fetchall())
    return settings
