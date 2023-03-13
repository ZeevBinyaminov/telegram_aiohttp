import os
import dotenv
import asyncio

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from parser.parser_async import run_parser

dotenv.load_dotenv()
API_TOKEN = os.getenv("API_TOKEN")

loop = asyncio.get_event_loop()
loop.create_task(run_parser())

storage = MemoryStorage()
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, loop=loop, storage=storage)
