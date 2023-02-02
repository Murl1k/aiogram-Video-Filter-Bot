from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from utils.utils import ExtendedKeyboard

back_to_menu = KeyboardButton('Назад в меню')
inline_back_to_menu = InlineKeyboardButton('Назад в меню', callback_data="back_to_menu")

# Клавиатура для администраторов
start_admin = ReplyKeyboardMarkup(resize_keyboard=True)
add_video_button = KeyboardButton('Добавить видео')
start_admin.add(add_video_button)

# Клавиатура для State добавления видео
stop_video_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
stop_video_button = KeyboardButton("Закончить добавление видео")
stop_video_keyboard.row(stop_video_button)

# Начальная клавиатура для юзеров
start_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
watch_video_button = KeyboardButton('Смотреть видео')
profile_button = KeyboardButton('Профиль')
help_button = KeyboardButton('/help')
start_keyboard.add(watch_video_button, profile_button, help_button)

# Клавиатура для просмотра видео
videos_keyboard = ExtendedKeyboard(resize_keyboard=True)
short_length = KeyboardButton('Короткие')
middle_length = KeyboardButton('Средние')
long_length = KeyboardButton('Длинные')
videos_keyboard.row(short_length, middle_length, long_length)
videos_keyboard.row(back_to_menu)
video_duration_row = videos_keyboard.get_row_values(videos_keyboard.find_row_by_button(short_length))

# Клавиатура профиля
profile_keyboard = InlineKeyboardMarkup()
settings_button = InlineKeyboardButton('Настройки', callback_data="profile_settings")
profile_keyboard.add(settings_button)


# Клавиатура настроек
profile_settings = InlineKeyboardMarkup()
setting_unique_videos = InlineKeyboardButton('Изменить сохранение видео', callback_data='setting_unique_video')
setting_clear_data = InlineKeyboardButton('Очистить просмотренные видео', callback_data='setting_clear_data')
back_to_profile = InlineKeyboardButton('Назад в профиль', callback_data='back_to_profile')
profile_settings.row(setting_unique_videos)
profile_settings.row(setting_clear_data)
profile_settings.row(back_to_profile)
