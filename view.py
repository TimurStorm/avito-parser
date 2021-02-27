import eel

import requests
import csv
import vk_api
import random
from time import sleep
from bs4 import BeautifulSoup
from datetime import datetime

token = '56036fde45f5c4e10920de4ad5d1b7c6bf4f78feb37395313eec5fa2acf991d43a7f2ae5ca0f4f9688213'
session = vk_api.VkApi('89172461399', '000168154Tim', token=token)
vk = session.get_api()


# функция отправки сообщения
def send_message(text):
    vk.messages.send(user_id=443194153, message=text, random_id=random.randint(-2147483648, +2147483647))


# находит объявления на сайте
def get_all_ads():
    page = requests.get("https://www.avito.ru/rossiya/knigi_i_zhurnaly?q=ёсикава")
    resp = datetime.now().strftime("%d %B, %H:%M") + ': ' + str(page)
    soup = BeautifulSoup(page.content, 'lxml').find('div', attrs={"data-marker": "catalog-serp"})
    ad = soup.find_all('div', attrs={'data-marker': 'item'})
    return ad, resp


# проверяет список объявлений на наличие новых предложений и в случае обнаружения присылает уведомление в лс в вк
@ eel.expose
def find_new_ads():
    ads_title = []
    with open('ads.csv', encoding='utf-8') as file:
        reader = csv.reader(file, delimiter=",")
        for row in reader:
            ads_title.append(row[0])
    while True:
        try:
            new_ad, resp = get_all_ads()
            for ad in new_ad:
                # ищем информацию о каждом объявлении
                info = ad.find('div', attrs={'class': "iva-item-body-NPl6W"})
                title_link = info.find('div', attrs={'class': "iva-item-titleStep-2bjuh"}) \
                    .find('a', attrs={'data-marker': 'item-title'})
                title = title_link.find('h3').get_text()

                # если объявления нет в списке
                if title not in ads_title:
                    link = 'https://www.avito.ru' + title_link.get('href')
                    send_message(text='New Book!' + '\n' + title + '\n' + link)
                    ads_title.append(title)
                    print('New Book!' + '\n' + title + '\n' + link)

                    # записываем в файл новое объявление
                    with open('ads.csv', mode="a", encoding='utf-8') as file:
                        writer = csv.DictWriter(file, delimiter=",", lineterminator="\r", fieldnames=['Title', 'Link'])
                        writer.writerow({'Title': title, 'Link': link})
                    sleep(2)
            return resp
        except Exception as e:
            return f'Ошибка : {e}'
        sleep(600)