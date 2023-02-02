from database.utils import auth_required
from database.sqlite import cursor, db
from aiogram import types
from keyboards import keyboards
from config import SHORT_VIDEO_LENGTH, MIDDLE_VIDEO_LENGTH, LONG_VIDEO_LENGTH
from database.profile import check_unique_videos, get_viewed_videos
import json


@auth_required
async def get_video(user: types.User, length: str, session_videos: set):
    """
    Получает видео с указанными параметрами.

    :param user: Пользователь (types.User)
    :param length: Длина видео (из кнопок клавиатуры (Короткие, Средние, Длинные))) (str)
    :param session_videos: Множество просмотренных видео из FSM
    :return: Возвращает ID видео, которое можно отправить в тг. Если видео по запросу не найдено, то вернет None
    """

    length_dict = {
        keyboards.short_length.text: SHORT_VIDEO_LENGTH,
        keyboards.middle_length.text: MIDDLE_VIDEO_LENGTH,
        keyboards.long_length.text: LONG_VIDEO_LENGTH
    }

    # Объединение минимальной и максимальной длины в список
    video_length = [length_dict[length][0], length_dict[length][1]]

    unique_videos = await check_unique_videos(user)
    user_viewed_videos = await get_viewed_videos(user)

    # Объединение видео
    viewed_videos = user_viewed_videos | session_videos if unique_videos else session_videos
    viewed_videos = list(viewed_videos)

    cursor.execute(
        f"""
        SELECT video_id FROM videos 
        WHERE (video_unique_id NOT IN ({('?,' * len(viewed_videos))[:-1]})) AND (duration > ? AND duration < ?)  
        ORDER BY RANDOM() 
        """,
        viewed_videos + video_length
    )

    try:
        return cursor.fetchone()[0]
    except TypeError:
        return None


@auth_required
async def save_viewed_video(user: types.User, videos_set: set):
    """
    Сохраняет видео пользователя в базу данных, указанные в множестве.

    :param user: Пользователь (types.User)
    :param videos_set: Множество просмотренных видео с FSM ViewedVideos (set)
    """

    if not (await check_unique_videos(user)):
        return

    videos = await get_viewed_videos(user) | videos_set

    # Превращаем множество в json, чтобы можно было хранить в базе данных
    videos = json.dumps(list(videos))

    cursor.execute(
        """
        UPDATE users 
        SET videos = ? 
        WHERE telegram_id = ?
        """,
        (videos, user.id)
    )
    db.commit()
