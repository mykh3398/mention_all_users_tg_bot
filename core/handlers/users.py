from aiogram import Bot, Dispatcher, F, Router, html
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command, CommandStart
from aiogram.fsm.state import State, StatesGroup


userCommandNamesGet = []
userCommandNamesPost = []
subscriptionNameRules = "Give a name for a new subscription AND REPLY TO THIS MESSAGE in format:\n\n<name of subscription>\n\nName could have more than one word but try to make it as brief as possible. Use only latin letters or numbers."

form_router = Router()


async def create_subscription_start(message: Message):
    await message.reply(subscriptionNameRules)
    #...test test2 test3


async def create_subscription_command(message: Message, state: FSMContext):
    #...
    await subscription # ??
    
    
async def subscription(message: Message, bot: Bot):
    CHAT_ID = message.chat.id    
    user = message.from_user
    chat_info = await bot.get_chat(CHAT_ID)
    pinnedMessageinfo = chat_info.pinned_message
    pinnedMessage = pinnedMessageinfo.text
    if pinnedMessage:
        if 'Bot' in pinnedMessage:
            new_text = f"SUBSCRIBERS:\nname:{user.first_name}, id:{user.id}"
        elif str(user.id) in pinnedMessage:
            return   
        else: 
            new_text = f"{pinnedMessage}\nname:{user.first_name}, id:{user.id}"
        await bot.edit_message_text(chat_id=CHAT_ID, message_id=pinnedMessageinfo.message_id, text=new_text, parse_mode='HTML')
    else:
        await bot.send_message(CHAT_ID, "В цьому чаті немає закріпленого повідомлення.")


async def mention_all(message: Message, bot: Bot):
    CHAT_ID = message.chat.id    
    user = message.from_user
    chat_info = await bot.get_chat(CHAT_ID)
    pinnedMessageinfo = chat_info.pinned_message
    pinnedMessage = pinnedMessageinfo.text
    #------------
    subscribers = []
    lines = pinnedMessage.split('\n')
    for line in lines:
        if 'name:' in line and 'id:' in line:
            name = line.split('name:')[1].split(',')[0].strip()
            user_id = int(line.split('id:')[1].strip())
            subscribers.append({'name': name, 'id': user_id})
    for subscriber in subscribers:
        if subscriber['id'] != user.id:
            user_link = f"<a href='tg://user?id={subscriber['id']}'>{subscriber['name']}</a>"  
            await bot.send_message(CHAT_ID, text=f'{user_link}', parse_mode='HTML')
    