from aiogram import Bot
from aiogram.types import Message

   
async def get_start(message: Message, bot: Bot):
    CHAT_ID = message.chat.id
    botMessage = await bot.send_message(CHAT_ID, text=f'Bot succesfully started!')
    await bot.pin_chat_message(CHAT_ID, botMessage.message_id)
     
    
async def get_hi(message: Message):
    #await bot.send_message(message.from_user.id, f'Привіт {message.from_user.first_name}!')
    #await message.answer (f"Привіт {message.from_user.first_name}")
    await message.reply (f"Привіт {message.from_user.first_name}!")
    