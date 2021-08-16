import eel
import settings

"""
Файл для вывода информациии на фронт
"""


def set_get():
    @eel.expose
    def get_parser_ads():

        # TODO: модифицировать до выдачи объектов Ad, избавиться от sql запроса

        resp = []
        parser_names = [parser.title for parser in settings.WORKING_PARSERS]
        try:
            for name in parser_names:
                settings.CURSOR.execute(f"""SELECT * from {name}""")
                info = settings.CURSOR.fetchall()
                info = [[i[0], i[2], name] for i in info]
                resp += info
        except TypeError:
            pass
        return resp

    @eel.expose
    def get_all_parsers():
        settings.CURSOR.execute(f"""SELECT name, timer from parsers""")
        info = settings.CURSOR.fetchall()
        info = [[i[0] for i in info], [i[1] for i in info]]
        return info

    @eel.expose
    def get_all_settings():
        settings.CURSOR.execute("""SELECT * from settings""")
        sett = dict(settings.CURSOR.fetchall())
        return sett
