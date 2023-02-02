from database.utils import auth_required
from database.sqlite import cursor, db
from keyboards import keyboards
from aiogram.utils import exceptions
from aiogram import types
import json


@auth_required
async def check_unique_videos(user: types.User):
    """
    Получает параметр пользователя, который отвечает за сохранение просмотренных видео.

    :param user: Пользователь (types.User)
    :return: Возвращает Boolean значение, сохранять видео при просмотре или нет
    """

    cursor.execute(f"SELECT unique_videos FROM users WHERE telegram_id = {user.id}")
    unique_videos = True if cursor.fetchone()[0] == 1 else False

    return unique_videos


@auth_required
async def get_viewed_videos(user: types.User):
    """
    Получает множество просмотренных видео пользователем

    :param user: Пользователь (types.User)
    :return: Возвращает множество просмотренных видео пользователем
    """

    cursor.execute(f"SELECT videos FROM users WHERE telegram_id = {user.id}")
    videos = json.loads(cursor.fetchone()[0])

    return set(videos)


@auth_required
async def change_setting(user: types.User, callback: types.CallbackQuery):
    """
    Функция принимает CallbackQuery от кнопки из профиля.

    :param user: Пользователь, у которого будет изменятся настройка (types.User)
    :param callback: CallbackQuery кнопки определенной настройки (types.CallbackQuery)
    :return: Возвращает значение, которое можно использовать в callback.answer
    """

    if callback.data == keyboards.setting_unique_videos.callback_data:
        cursor.execute(f"""
                        UPDATE users 
                        SET unique_videos = (CASE WHEN unique_videos = 1 THEN 0 ELSE 1 END)
                        WHERE telegram_id = {user.id}
                        """
                       )
        callback_answer = "Вы успешно изменили настройку исключения повторяющихся видео!"

    elif callback.data == keyboards.setting_clear_data.callback_data:
        cursor.execute(f"""
                        UPDATE users
                        SET videos = ?
                        WHERE telegram_id = {user.id}
                        """,
                       ('[]', )
                       )
        callback_answer = "Данные о просмотренных видео успешно очищены!"

    else:
        raise exceptions.NotFound("Указанная настройка не найдена!")

    db.commit()

    return callback_answer
