from random import randint
from settings import VK_SESSION


def send_message(text):
    VK_SESSION.messages.send(
        user_id=443194153,
        message=text,
        random_id=randint(-2147483648, +2147483647),
    )
