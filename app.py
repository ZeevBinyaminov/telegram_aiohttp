from aiogram import executor
from loader import dp
from handlers import tutor


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
