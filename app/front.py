import eel
from settings import ACTIVE_PARSERS

"""
Файл для вывода информациии на фронт
"""


@eel.expose
def get_parser_info(parser_title: str):
    parser = ACTIVE_PARSERS[parser_title]
    return vars(parser)


@eel.expose
def get_parser_ads(parser_title: str):
    parser = ACTIVE_PARSERS[parser_title]
    info = {}
    for ad in parser.ads:
        info[ad.title] = vars(ad)
    return info


@eel.expose
def get_all_parsers():
    return ACTIVE_PARSERS


@eel.expose
def get_all_settings():
    pass
