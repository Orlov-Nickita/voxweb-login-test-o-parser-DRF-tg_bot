import os

import requests
from dotenv import set_key
from loader import bot, dp
from aiogram.types import ParseMode, Message
from keyboards import RKM_for_the_menu


@dp.message_handler(commands=['start'])
async def send_welcome_func(message: Message) -> None:
    """
    Отправляет Пользователю стартовое сообщение
    :param message: В качестве параметра передается сообщение из чата
    :type message: aiogram.types.Message
    :return: Отправляется сообщение в чат
    :rtype aiogram.types.Message
    """
    chat_id = message.chat.id

    set_key(dotenv_path='.env', key_to_set='CHAT_ID', value_to_set=str(chat_id))
    
    url = os.getenv('URL_FOR_BOT_NOTIFICATION')
    
    response = requests.post(url=url, data={'id': chat_id})
    await bot.send_message(chat_id=message.chat.id,
                           text=f'Ваш ID: <code>{message.chat.id}</code>\n'
                                f'{response.json()}',
                           parse_mode=ParseMode.HTML,
                           reply_markup=RKM_for_the_menu())
    

@dp.message_handler(content_types=['text'])
async def text_func(message: Message) -> None:
    """
    Функция, которая реагирует на сообщение пользователя из чата.
    :param message: В качестве параметра передается сообщение из чата
    :type message: aiogram.types.Message
    :return: None
    :rtype: aiogram.types.Message

    """
    if message.text.startswith('Список товаров'):
        pass
    
    else:
        await bot.send_message(chat_id=message.chat.id,
                               text='Выберите пункт меню\n')
