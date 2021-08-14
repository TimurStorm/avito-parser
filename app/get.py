import eel
import settings

"""
Файл для вывода информациии на фронт
"""


def set_get():
    @eel.expose
    def get_parser_ads(parsers_names: list):
        resp = []
        for name in parsers_names:
            settings.CURSOR.execute(f"""SELECT * from {name}""")
            info = settings.CURSOR.fetchall()
            info = [[i[0], i[2]] for i in info]
            resp += info
        return resp

    @eel.expose
    def get_all_parsers():
        settings.CURSOR.execute(f"""SELECT name from parsers""")
        info = settings.CURSOR.fetchall()
        info = [i[0] for i in info]
        return info

    @eel.expose
    def get_all_settings():
        settings.CURSOR.execute("""SELECT * from settings""")
        sett = dict(settings.CURSOR.fetchall())
        return sett
