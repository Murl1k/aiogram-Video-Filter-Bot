from database.utils import auth_required
from database.sqlite import cursor, db
from aiogram import types


@auth_required
async def save_video(user: types.User, video: types.Video):
    """Добавляет видео в базу данных

    :param video: Видео, прикрепленное к сообщению (types.Video)
    :param user: Пользователь, добавивший видео (types.User)
    :return: Возвращает 1, если видео успешно добавлено в базу, и 0, если не добавлено.
    """

    cursor.execute(f"SELECT * FROM videos WHERE video_unique_id = '{video.file_unique_id}'")
    if cursor.fetchone():
        print(f"Видео {video.file_unique_id} уже есть в базе данных")
        return 0

    cursor.execute("""INSERT INTO videos VALUES(?, ?, ?, ?, ?, ?, ?)""",
                   (None, video.file_unique_id, video.file_id, video.file_name,
                    video.duration, video.file_size, user.id))

    print(f"({user.id}) Добавлено видео в базу данных: Filename: {video.file_name}, unique_id {video.file_unique_id}, "
          f"Size: {video.file_size}, Duration: {video.duration}, Id: {video.file_id}")

    db.commit()

    return 1
