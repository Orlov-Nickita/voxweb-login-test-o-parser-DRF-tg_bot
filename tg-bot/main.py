from message_handler import *
from aiogram.utils import executor

if __name__ == '__main__':
    print('Бот запущен')
    executor.start_polling(dispatcher=dp)