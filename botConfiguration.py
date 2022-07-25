from aiogram import Dispatcher, Bot
from aiogram.contrib.fsm_storage.memory import MemoryStorage

TOKEN =  'your token'

bot = Bot(TOKEN)


dp = Dispatcher(bot, storage = MemoryStorage())