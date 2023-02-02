from aiogram import types, Dispatcher
from config import MAX_VIDEO_PER_SESSION, SHORT_VIDEO_LENGTH, MIDDLE_VIDEO_LENGTH, LONG_VIDEO_LENGTH
from bot import bot
from database.utils import is_user_in_database, register_user
from keyboards import keyboards


async def start(message: types.Message):
    if not is_user_in_database(message.from_user):
        await register_user(message.from_user)

    await bot.send_message(message.chat.id, "Привет!", reply_markup=keyboards.start_keyboard)


async def help(message: types.Message):
    await message.reply(
        f"""
<b>Помощь в пользовании ботом.</b>

<b>Пояснение к настройкам профиля. </b>

<b>Изменить сохранение видео</b> - Если включено, 
то после окончания сессии просмотра видео будут сохранятся просмотренные вами видео в базу данных. 
Если при просмотре видео пишет, что закончились видео,
то нужно будет очистить данные о просмотренных видео.

<b>Очистить просмотренные видео</b> - удаляются все вами просмотренные видео из базы данных


<b>Администраторские команды.</b> /admin

<b>Добавить видео</b> - нужно переслать боту какое-либо видео, тогда он добавит его в базу данных.
За одну сессию нельзя добавить больше {MAX_VIDEO_PER_SESSION}.


<b>Пользовательские команды.</b>

<b>Просмотр видео</b> - можно просматривать видео из базы данных по выбранной длине.
(Короткие - от {SHORT_VIDEO_LENGTH[0]} до {SHORT_VIDEO_LENGTH[1]} с.,
Средние - от {MIDDLE_VIDEO_LENGTH[0]} до {MIDDLE_VIDEO_LENGTH[1]} с.,
Длинные - от {LONG_VIDEO_LENGTH[0]} до {LONG_VIDEO_LENGTH[1]} с.)
""",
        parse_mode='html')


def register_handlers_other(dispatcher: Dispatcher):
    dispatcher.register_message_handler(help, commands='help')
    dispatcher.register_message_handler(start, commands=['start'])
