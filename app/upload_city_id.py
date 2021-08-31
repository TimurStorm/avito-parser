import os
import sqlite3
from pathlib import Path
from transliterate import translit
import requests
import bs4
from random import choice, randint
from time import sleep

DIR_PATH = str(Path(os.getcwd()).parent)
CONN = sqlite3.connect(database=DIR_PATH + '\\data\\database.db')
CURSOR = CONN.cursor()
CURSOR.execute("""CREATE TABLE IF NOT EXISTS city (ru_name, en_name, city_id)""")
session = requests.session()

headers = { 'authority': 'm.avito.ru',
            'pragma': 'no-cache',
            'cache-control': 'no-cache',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Mobile Safari/537.36',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'sec-fetch-site': 'none',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-user': '?1',
            'sec-fetch-dest': 'document',
            'accept-language': 'ru-RU,ru;q=0.9',
            'cookie': '__cfduid=da6b6b5b9f01fd022f219ed53ac3935791610912291; sessid=ef757cc130c5cd228be88e869369c6'
                      '54.1610912291; _ga=GA1.2.559434019.1610912292; _gid=GA1.2.381990959.1610912292; _fbp=fb.1.16'
                      '10912292358.1831979940; u=2oiycodt.1oaavs8.dyu0a4x7fxw0; v=1610912321; buyer_laas_location=6'
                      '41780; buyer_location_id=641780; luri=novosibirsk; buyer_selected_search_radius4=0_general; '
                      'buyer_local_priority_v2=0; sx=H4sIAAAAAAACAxXLQQqAIBAF0Lv8dYvRLEdvU0MIBU0iKCHePXr71zGfefd1W5R'
                      'LYick2kSakiB2VETclpf85n19RJMSp4vJOSlM%2F2BMOBDNaigE9taM8QH0oydNVAAAAA%3D%3D; dfp_group=100; _'
                      'ym_uid=1610912323905107257; _ym_d=1610912323; _ym_visorc_34241905=b; _ym_isad=2; _ym_visorc_41'
                      '9506=w; _ym_visorc_188382=w; __gads=ID=2cff056a4e50a953-22d0341a94b900a6:T=1610912323:S=ALNI_MZ'
                      'MbOe0285QjW7EVvsYtSa-RA_Vpg; f=5.8696cbce96d2947c36b4dd61b04726f1a816010d61a371dda816010d61a371d'
                      'da816010d61a371dda816010d61a371ddbb0992c943830ce0bb0992c943830ce0bb0992c943830ce0a816010d61a371d'
                      'd2668c76b1faaa358c08fe24d747f54dc0df103df0c26013a0df103df0c26013a2ebf3cb6fd35a0ac0df103df0c260'
                      '13a8b1472fe2f9ba6b978e38434be2a23fac7b9c4258fe3658d831064c92d93c3903815369ae2d1a81d04dbcad294c'
                      '152cb0df103df0c26013a20f3d16ad0b1c5462da10fb74cac1eab2da10fb74cac1eab3c02ea8f64acc0bdf0c7705'
                      '2689da50d2da10fb74cac1eab2da10fb74cac1eab2da10fb74cac1eab2da10fb74cac1eab91e52da22a560f5503c77'
                      '801b122405c48ab0bfc8423929a6d7a5083cc1669877def5708993e2ca678f1dc04f891d61e35b0929bad7c1e'
                      'a5dec762b46b6afe81f200c638bc3d18ce60768b50dd5e12c30e37135e8f7c6b64dc9f90003c0354a346b8ae4e81a'
                      'cb9fa46b8ae4e81acb9fa02c68186b443a7acf8b817f3dc0c3f21c1eac53cc61955882da10fb74cac1eab2d'
                      'a10fb74cac1eab5e5aa47e7d07c0f95e1e792141febc9cb841da6c7dc79d0b'}
session.headers.update(headers)

CURSOR.execute("""SELECT ru_name from city""")
s = CURSOR.fetchall()
s = [i[0] for i in s]
print(s)

city = []
pages = ['nedvizhimost', 'transport', 'rabota', 'predlozheniya_uslug', 'bytovaya_elektronika', 'hobbi_i_otdyh']

responce = session.get('https://en.wikipedia.org/wiki/List_of_cities_and_towns_in_Russia')
soup = bs4.BeautifulSoup(responce.text, 'lxml').find('tbody')
trs = soup.find_all('tr')
trs.pop(0)

for tr in trs:
    tds = tr.find_all('td')
    ru_name = tds[1].get_text().lower()
    if ru_name in s:
        continue
    try:
        en_name = tds[0].get_text()

        responce = session.get(f'https://www.avito.ru/{en_name}/{choice(pages)}')
        if responce.status_code != 200:
            raise AttributeError

    except AttributeError:
        en_name = translit(ru_name, language_code='ru', reversed=True)
        responce = session.get(f'https://www.avito.ru/{en_name}/{choice(pages)}')

    soup = bs4.BeautifulSoup(responce.text, 'lxml')
    soup = soup.find_all('script')
    soup = [str(script) for script in soup]

    target_string = ''

    for script in soup:
        if 'locationId' in script:
            target_string = script
            break

    target_list = target_string.split('%22')
    city_id = 0
    for elem_index in range(len(target_list)):
        if target_list[elem_index] == 'locationId' and target_list[elem_index + 1] == '%3A':
            city_id = target_list[elem_index + 2]
            break
    if city_id != 0:
        print('----------------------------------')
        print(f'{ru_name} {en_name} {city_id}')
        CURSOR.execute(
            f"INSERT INTO city VALUES (?,?,?)", [ru_name, en_name, city_id]
        )
        CONN.commit()

    else:
        print(f'{en_name} {responce}')
    sleep(randint(2, 4))