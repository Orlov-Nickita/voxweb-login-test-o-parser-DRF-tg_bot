from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def RKM_for_the_menu() -> ReplyKeyboardMarkup:
    """
    Клавиатура с кнопками меню бота
    :return: При нажатии отправляется сообщение в чат и бот обрабатывает полученное сообщение
    """
    rkm_menu = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    rkm_menu.add(KeyboardButton('Список товаров'))
    return rkm_menu

