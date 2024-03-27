from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.filters import Command

import asyncio
import logging

from core.handlers.basic import get_start
from core.handlers.basic import get_hi
from core.handlers.users import subscription
from core.handlers.users import mention_all
from core.handlers.users import create_subscription

from core.utils.commands import set_commands

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
    
    dp.message.register(get_start, Command(commands=['start']))
    dp.message.register(get_hi, Command(commands=['hi']))
    dp.message.register(mention_all, Command(commands=['all']))
    dp.message.register(subscription, Command(commands=['subscribe']))
    dp.message.register(create_subscription, Command(commands=['create_subscription']))
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
    
