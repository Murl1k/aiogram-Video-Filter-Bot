from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import exceptions
from utils.utils import admin_command
from config import MAX_VIDEO_PER_SESSION
from keyboards import keyboards
from bot import bot
from database.admin import save_video


@admin_command
async def admin_start(message: types.Message):
    await bot.send_message(message.chat.id, "Привет!", reply_markup=keyboards.start_admin)


class WaitForVideo(StatesGroup):
    amount = State()
    successfully_added = State()


@admin_command
async def add_video(message: types.Message):
    await WaitForVideo.amount.set()
    await message.reply(f"Посылай видео, а я буду добавлять их в базу данных. В базу нельзя добавлять одинаковые видео."
                        f" За одну сессию можно отправить не болeе {MAX_VIDEO_PER_SESSION} видео.",
                        reply_markup=keyboards.stop_video_keyboard)


@admin_command
async def stop_video(message: types.Message, state: FSMContext):
    current_state = await state.get_state()

    if current_state is None:
        await message.reply("Запустите добавление видео снова.", reply_markup=keyboards.start_admin)
        return

    async with state.proxy() as data:
        successfully_added = data.get('successfully_added', 0)

    await state.finish()
    await message.reply(f"Закончено. Всего успешно добавлено {successfully_added} видео",
                        reply_markup=keyboards.start_admin)


@admin_command
async def process_video(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        amount = data.get('amount', 0) + 1
        successfully_added = data.get('successfully_added', 0)
        data['amount'] = amount

    try:
        if amount > MAX_VIDEO_PER_SESSION:
            await message.reply(f"За одну сессию нельзя добавлять более {MAX_VIDEO_PER_SESSION} видео."
                                f"Успешно добавлено {successfully_added} видео."
                                f" Сессия окончена.",
                                reply_markup=keyboards.start_admin)
            await state.finish()

        else:
            if (MAX_VIDEO_PER_SESSION - amount) % 10 == 0:
                await message.reply(f"Вы можете добавить еще {MAX_VIDEO_PER_SESSION - amount} видео")

            video = message.video

            result = await save_video(message.from_user, video)

            async with state.proxy() as data:
                data['successfully_added'] = successfully_added + result

    except exceptions.RetryAfter:
        pass


@admin_command
async def process_video_fail(message: types.Message):
    try:
        await message.reply("Сообщение должно содержать видео!")
    except exceptions.RetryAfter:
        pass


def register_handlers_admin(dispatcher: Dispatcher):
    dispatcher.register_message_handler(admin_start, commands=['admin'])
    dispatcher.register_message_handler(add_video, lambda mess: mess.text == keyboards.add_video_button.text)
    dispatcher.register_message_handler(stop_video, lambda mess: mess.text == keyboards.stop_video_button.text,
                                        state="*")
    dispatcher.register_message_handler(process_video, state=WaitForVideo.amount, content_types=types.ContentType.VIDEO)
    dispatcher.register_message_handler(process_video_fail, state=WaitForVideo.amount)
