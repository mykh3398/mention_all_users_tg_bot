from aiogram import Bot, Dispatcher, types, Router
from aiogram.types import Message
from aiogram.filters import Command

import asyncio
import logging

from core.utils.commands import set_commands
from core.handlers.basic import basic_router
from core.handlers.users import users_router

from config import API_TOKEN
from config import TESTING_CHAT_ID



bot = Bot(token=API_TOKEN)
dp = Dispatcher()


async def start_bot(bot: Bot): 
    await set_commands(bot)
    await bot.send_message(TESTING_CHAT_ID, text='✅ Бот запущено!')
                              
async def stop_bot(bot: Bot): 
    await bot.send_message(TESTING_CHAT_ID, text="❌ Бот зупинено!")
    

async def start():
    logging.basicConfig(level=logging.INFO, 
                        format="%(asctime)s - [%(levelname)s] - %(name)s - "
                        "(%(filename)s).%(funcName)s(%(lineno)d) - %(message)s"
                        )
    dp.startup.register(start_bot)
    dp.shutdown.register(stop_bot)
    dp.include_router(basic_router)
    dp.include_router(users_router)

    # for userCommand in userCommands:
    #     dp.message.register(subscription, Command(commands=['subscribe']))
    
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

        
if __name__ == "__main__":
    try:
       asyncio.run(start()) 
    except KeyboardInterrupt:
        print("Exit")
    
