from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from functools import wraps
from config import ADMIN_USERS


class ExtendedKeyboard(ReplyKeyboardMarkup):
    """ Расширяет дефолтный класс клавиатуры"""

    def get_row_values(self, row: int):
        """
        Получает значения кнопок указанного ряда.

        :param row: Номер ряда клавиатуры (отсчет с нуля)
        """

        try:
            row_list = self["keyboard"][row]
        except IndexError:
            return None

        try:
            return tuple(button.text for button in row_list)
        except AttributeError:
            return tuple(row_list)

    def find_row_by_button(self, button: KeyboardButton):
        """
        Возвращает ряд, в котором будет найдена указанная кнопка

        :param button: Кнопка, которую нужно найти
        """

        for row, row_list in enumerate(self["keyboard"]):
            if button in row_list:
                return row
        else:
            return None


def is_user_admin(user_id):
    """ Является ли пользователь админом.

    :param user_id: ID пользователя
    """

    return user_id in ADMIN_USERS


def admin_command(func):
    """
    Декоратор для админских команд.
    Команда будет исполнена, если пользователь есть в списке ADMIN_USERS в config.py.
    """

    @wraps(func)
    async def wrapper(*args, **kwargs):
        user_id = args[0].from_user.id
        if is_user_admin(user_id):
            return await func(*args, **kwargs)

    return wrapper
