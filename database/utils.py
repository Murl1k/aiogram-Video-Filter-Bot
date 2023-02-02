from aiogram import types
from database.sqlite import cursor, db
from functools import wraps


def is_user_in_database(user: types.User):
    """
    Проверяет, есть ли пользователь в базе данных

    :param user: Пользователь (types.User)
    :return: Возвращает значение True или False.
    """

    cursor.execute(f"""SELECT * FROM users where telegram_id = {user.id}""")

    if cursor.fetchone():
        return True
    else:
        return False


async def register_user(user: types.User):
    """
    Регистрация пользователя в базу данных.

    :param user: Объект пользователя types.User
    """

    cursor.execute("""INSERT INTO users VALUES (?, ?, ?, ?)""", (None, user.id, "[]", 1))
    db.commit()
    print(f"{user.full_name} только что зарегистрировался")


def auth_required(func):
    """
    Декоратор асинхронных функций. В аргументах функции обязательно должен быть объект types.User
    Проверяет, есть ли пользователь в базе данных, если его нет, то регистрирует.
    """

    @wraps(func)
    async def wrapper(*args, **kwargs):
        for arg in args:
            if isinstance(arg, types.User):
                user = arg
                break
        else:
            user = None

        if not is_user_in_database(user):
            await register_user(user)

        return await func(*args, **kwargs)

    return wrapper
