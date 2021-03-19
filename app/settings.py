import asyncio
import os
import vk_api
from pathlib import Path

WIND_SIZE = (800, 600)

DIR_PATH = str(Path(os.getcwd()).parent)

token = "56036fde45f5c4e10920de4ad5d1b7c6bf4f78feb37395313eec5fa2acf991d43a7f2ae5ca0f4f9688213"
session = vk_api.VkApi("89172461399", "000168154Tim", token=token)
VK = session.get_api()

ACTIVE_PARSERS = []

MAIN_LOOP = asyncio.get_event_loop()
