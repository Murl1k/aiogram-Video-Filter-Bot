import middlewares
from aiogram import executor
from bot import dp
from handlers import client, admin, other, profile
from database import sqlite

admin.register_handlers_admin(dp)
client.register_handlers_client(dp)
other.register_handlers_other(dp)
profile.register_handlers_profile(dp)


async def on_ready(_):
    await sqlite.db_start()
    middlewares.setup(dp)

    print('Я запустился!')

executor.start_polling(dp, on_startup=on_ready)
