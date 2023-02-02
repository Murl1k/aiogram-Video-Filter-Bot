from middlewares import throttling
from aiogram import Dispatcher


def setup(dp: Dispatcher):
    dp.middleware.setup(throttling.ThrottlingMiddleware())
