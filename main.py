import asyncio
from aiogram import executor
from botConfiguration import dp
from handlers import client, admin
from handlers.data_base import postgre_db


asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

async def checkWork(_):
    print("Bot is working")
    await postgre_db.sql_start_work()
    
admin.register_handlers_admin(dp = dp)

client.register_handlers_client(dp = dp)


executor.start_polling(skip_updates = True,dispatcher = dp, on_startup=checkWork)