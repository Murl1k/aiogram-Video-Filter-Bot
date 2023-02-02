from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from keyboards import keyboards
from bot import bot
from database.client import get_video, save_viewed_video
from utils.misc.throttling import rate_limit


# Команды просмотра видео

# FSM, которая собирает просмотренные видео
class ViewedVideos(StatesGroup):
    videos_set = State()


async def watch_videos(message: types.Message):
    await ViewedVideos.videos_set.set()
    await bot.send_message(message.chat.id, "Ты можешь смотреть видео любой длины. Выбери из предложенных",
                           reply_markup=keyboards.videos_keyboard)


async def watch_videos_error(message: types.Message):
    await message.reply('Перезапусти просмотр видео, произошла ошибка', reply_markup=keyboards.start_admin)


async def stop_watching(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        videos = data.get('videos_set', set())

    if len(videos) > 0:
        await save_viewed_video(message.from_user, videos)

    if await state.get_state():
        await state.finish()

    await bot.send_message(message.chat.id, "Меню", reply_markup=keyboards.start_keyboard)


@rate_limit(limit=1)
async def viewed_videos_process(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        videos_set = data.get('videos_set', set())

        # Получаем видео, которое еще не смотрел пользователь (В сессии, или в общем, в зависимости от настройки
        # пользователя)
        video_id = await get_video(message.from_user, message.text, videos_set)

        if video_id:
            sent_message = await bot.send_video(chat_id=message.from_user.id, video=video_id)
            videos_set.add(sent_message.video.file_unique_id)
        else:
            await message.reply(f"{message.text} видео закончились."
                                f" Перезапусти просмотр видео(если отключена настройка исключения одинаковых видео), "
                                f"либо очисти данные о просмотренных видео в настройках профиля.")

        data['videos_set'] = videos_set


def register_handlers_client(dispatcher: Dispatcher):
    dispatcher.register_message_handler(
        watch_videos,
        lambda m: m.text == keyboards.watch_video_button.text
    )
    dispatcher.register_message_handler(
        watch_videos_error,
        lambda m: m.text in keyboards.video_duration_row or m.text == keyboards.back_to_menu.text,
        state=None
    )
    dispatcher.register_message_handler(
        stop_watching,
        lambda mess: mess.text == keyboards.back_to_menu.text,
        state=ViewedVideos.videos_set
    )
    dispatcher.register_message_handler(
        viewed_videos_process,
        state=ViewedVideos.videos_set
    )
