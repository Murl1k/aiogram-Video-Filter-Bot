from aiogram import Dispatcher, Bot
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils import exceptions
from os import environ

try:
    bot = Bot(token=environ.get('TOKEN'))
    dp = Dispatcher(bot, storage=MemoryStorage())

except exceptions.ValidationError:
    print("Вы не установили токен бота в виртуальное окружение или ввели его неправильно.")
    quit()
