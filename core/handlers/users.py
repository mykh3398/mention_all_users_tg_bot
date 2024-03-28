from aiogram import Bot, Dispatcher, F, Router, html
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import (
    KeyboardButton,
    Message,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
)
import logging

userCommandNamesGet = []
userCommandNamesPost = []
subscriptionNameRules = "Give a name for a new subscription AND REPLY TO THIS MESSAGE in format:\n\n<name of subscription>\n\nName could have more than one word but try to make it as brief as possible. Use only latin letters or numbers."

users_router = Router()

class SunscriptionForm(StatesGroup):
    name = State()

    
@users_router.message(Command('create_subscription'))
async def create_subscription_name(message: Message, state: FSMContext) -> None:
    await state.set_state(SunscriptionForm.name)
    await message.answer(subscriptionNameRules,
        reply_markup=ReplyKeyboardRemove()) #haven't tested yet


@users_router.message(SunscriptionForm.name)
async def process_subscription_name(message: Message, state: FSMContext, bot: Bot) -> None:
    await state.update_data(name=message.text)
    CHAT_ID = message.chat.id
    pinnedMessageinfo = await find_pinned_message(message, bot)
    
    if " " in message.text:
        userMessage = message.text.replace(' ', '_').lower()
    else:
        userMessage = message.text.lower()
        
    if pinnedMessageinfo:
        userMessageUpper = message.text.upper()
        if userMessageUpper in pinnedMessageinfo.text:
            await bot.send_message(CHAT_ID, "Name of the subscription already exists")   
        else:
            new_text = f"{pinnedMessageinfo.text}\n\n{userMessageUpper}:"
            await bot.edit_message_text(chat_id=CHAT_ID, message_id=pinnedMessageinfo.message_id, text=new_text, parse_mode='HTML')
            await bot.send_message(CHAT_ID, f"Subscription {userMessage} succesfully created! To subscribe type:\n/subscribe_{userMessage}")
    else:
        await bot.send_message(CHAT_ID, "There's no any pinned message.")


#function for processing user input ?

#function for creating or algorithm for subscribe_<name> command  
    
#function for creating or algorithm for all_<name> command      
    
 
async def find_pinned_message(message: Message, bot: Bot):
    CHAT_ID = message.chat.id    
    chat_info = await bot.get_chat(CHAT_ID)
    pinnedMessageinfo = chat_info.pinned_message
    return pinnedMessageinfo
 
       
@users_router.message(Command("subscribe"))    
async def subscription(message: Message, bot: Bot):
    CHAT_ID = message.chat.id    
    user = message.from_user
    pinnedMessageinfo = await find_pinned_message(message, bot)
    if pinnedMessageinfo:
        if 'Bot' in pinnedMessageinfo.text:
            new_text = f"ALL:\nname:{user.first_name}, id:{user.id}"
        elif str(user.id) in pinnedMessageinfo.text:
            return   
        else: 
            new_text = f"{pinnedMessageinfo.text}\nname:{user.first_name}, id:{user.id}"
        await bot.edit_message_text(chat_id=CHAT_ID, message_id=pinnedMessageinfo.message_id, text=new_text, parse_mode='HTML')
    else:
        await bot.send_message(CHAT_ID, "В цьому чаті немає закріпленого повідомлення.")


async def authoritarian_subscription(message: Message, bot: Bot):
    CHAT_ID = message.chat.id    
    user = message.from_user.id
    
    #function of manually subscribing users by admin (??)
    #probably FSM is also needed
    
    pinnedMessageinfo = await find_pinned_message(message, bot)
    if pinnedMessageinfo:
        if str(user) in pinnedMessageinfo.text:
            return   
        else: 
            new_text = f"{pinnedMessageinfo.text}\nname:{user.first_name}, id:{user}"
        await bot.edit_message_text(chat_id=CHAT_ID, message_id=pinnedMessageinfo.message_id, text=new_text, parse_mode='HTML')

    
@users_router.message(Command("all"))
async def mention_all(message: Message, bot: Bot):
    CHAT_ID = message.chat.id    
    user = message.from_user
    chat_info = await bot.get_chat(CHAT_ID)
    pinnedMessageinfo = chat_info.pinned_message
    pinnedMessage = pinnedMessageinfo.text
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
    
    
@users_router.message(Command("cancel"))
@users_router.message(F.text.casefold() == "cancel")
async def cancel_handler(message: Message, state: FSMContext) -> None:
    """
    Allow user to cancel any action
    """
    current_state = await state.get_state()
    if current_state is None:
        return

    logging.info("Cancelling state %r", current_state)
    await state.clear()
    await message.answer(
        "Cancelled.",
        reply_markup=ReplyKeyboardRemove(),
    )#haven't tested yet