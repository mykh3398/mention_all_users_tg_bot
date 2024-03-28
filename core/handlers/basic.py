from aiogram import Bot, Router
from aiogram.filters import Command
from aiogram.types import Message


basic_router = Router()

@basic_router.message(Command("start"))   
async def get_start(message: Message, bot: Bot):
    CHAT_ID = message.chat.id
    botMessage = await bot.send_message(CHAT_ID, text=f'Bot succesfully started!')
    await bot.pin_chat_message(CHAT_ID, botMessage.message_id)
     
     
@basic_router.message(Command("hi"))    
async def get_hi(message: Message):
    #await message.answer (f"Привіт {message.from_user.first_name}")
    await message.reply (f"Привіт {message.from_user.first_name}!")
    