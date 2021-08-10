import eel
import settings

"""
Файл для вывода информациии на фронт
"""


def set_get():
    @eel.expose
    def get_parser_ads(parser_name: str):
        settings.CURSOR.execute(f"""SELECT * from '{parser_name}'""")
        info = settings.CURSOR.fetchall()
        info = [list(i) for i in info]
        return {parser_name: info}

    @eel.expose
    def get_all_parsers():
        settings.CURSOR.execute(f"""SELECT name from parsers""")
        info = settings.CURSOR.fetchall()
        info = [list(i) for i in info]
        return info

    @eel.expose
    def get_all_settings():
        settings.CURSOR.execute("""SELECT * from settings""")
        sett = dict(settings.CURSOR.fetchall())
        return sett
