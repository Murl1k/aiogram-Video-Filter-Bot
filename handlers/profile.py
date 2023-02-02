from aiogram import types, Dispatcher
from aiogram.utils import exceptions
from utils.utils import is_user_admin
from keyboards import keyboards
from database.profile import check_unique_videos, get_viewed_videos, change_setting
from bot import bot


profile_settings_list = [keyboards.setting_clear_data.callback_data, keyboards.setting_unique_videos.callback_data]


# Команды профиля
async def profile(message: types.Message):
    user_status = "admin" if is_user_admin(message.from_user.id) else "user"

    await bot.send_message(
        message.from_user.id,
        f"👤 <b>Профиль пользователя: {message.from_user.full_name}</b>\n\n"
        f"🆔 ID пользователя: {message.from_user.id} \n"
        f"💼 Статус: {user_status}\n",
        reply_markup=keyboards.profile_keyboard,
        parse_mode="HTML"
    )


async def back_to_profile(callback: types.CallbackQuery):
    user_status = "admin" if is_user_admin(callback.from_user.id) else "user"

    await bot.edit_message_text(
        f"👤 <b>Профиль пользователя: {callback.from_user.full_name}</b>\n\n"
        f"🆔 ID пользователя: {callback.from_user.id} \n"
        f"💼 Статус: {user_status}\n",
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        reply_markup=keyboards.profile_keyboard,
        parse_mode="HTML"
    )


# Команды настроек профиля
async def profile_settings_process(callback: types.CallbackQuery):
    if callback.data in profile_settings_list:
        callback_answer = await change_setting(callback.from_user, callback)
        await callback.answer(callback_answer, show_alert=True)

    save_video = await check_unique_videos(callback.from_user)
    videos = await get_viewed_videos(callback.from_user)

    try:
        await bot.edit_message_text(
            f"<b>Настройки профиля</b>\n\u200b\n"
            f"⚙ Исключить повторяющиеся видео: <b>{save_video}</b>\n"
            f"📊 Просмотрено видео(разных): <b>{len(videos)}</b>\n",
            chat_id=callback.from_user.id,
            message_id=callback.message.message_id,
            reply_markup=keyboards.profile_settings,
            parse_mode="HTML"
        )
    except exceptions.MessageNotModified:
        pass


def register_handlers_profile(dispatcher: Dispatcher):
    dispatcher.register_message_handler(
        profile,
        lambda m: m.text == keyboards.profile_button.text
    )

    dispatcher.register_callback_query_handler(
        profile_settings_process,
        lambda c: c.data in profile_settings_list or c.data == "profile_settings"
    )
    dispatcher.register_callback_query_handler(
        back_to_profile,
        lambda c: c.data == "back_to_profile"
    )
