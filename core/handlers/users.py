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

form_router = Router()

class SunscriptionForm(StatesGroup):
    name = State()


# async def command_start(message: Message, state: FSMContext) -> None:
#     await state.set_state(SunscriptionForm.name)
#     await message.answer(
#         "Hi there! What's your name?",
#         reply_markup=ReplyKeyboardRemove(),
#     )
    
    
@form_router.message(Command('create_subscription'))
async def create_subscription_name(message: Message, state: FSMContext) -> None:
    await state.set_state(SunscriptionForm.name)
    await message.answer(subscriptionNameRules,
        reply_markup=ReplyKeyboardRemove()) #haven't tested yet


@form_router.message(Command("cancel"))
@form_router.message(F.text.casefold() == "cancel")
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
    

async def process_subscription_name(message: Message, state: FSMContext) -> None:
    await state.update_data(name=message.text)
    #await state.set_state(SunscriptionForm.<state>)
    await message.answer(
        f"Subscription {html.quote(message.text)} have been created!",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text="Yes"),
                    KeyboardButton(text="No"),
                ]
            ],
            resize_keyboard=True,
        ),
    )#haven't tested yet
 
 
async def find_pinned_message(message: Message, bot: Bot):
    CHAT_ID = message.chat.id    
    chat_info = await bot.get_chat(CHAT_ID)
    pinnedMessageinfo = chat_info.pinned_message
    return pinnedMessageinfo
       
    
async def subscription(message: Message, bot: Bot):
    CHAT_ID = message.chat.id    
    user = message.from_user
    pinnedMessageinfo = await find_pinned_message(message, bot)
    if pinnedMessageinfo:
        await authorithorian_subscription(message, bot)
        if 'Bot' in pinnedMessageinfo.text:
            new_text = f"SUBSCRIBERS:\nname:{user.first_name}, id:{user.id}"
        elif str(user.id) in pinnedMessageinfo.text:
            return   
        else: 
            new_text = f"{pinnedMessageinfo.text}\nname:{user.first_name}, id:{user.id}"
        await bot.edit_message_text(chat_id=CHAT_ID, message_id=pinnedMessageinfo.message_id, text=new_text, parse_mode='HTML')
    else:
        await bot.send_message(CHAT_ID, "В цьому чаті немає закріпленого повідомлення.")


async def authorithorian_subscription(message: Message, bot: Bot):
    CHAT_ID = message.chat.id    
    kirilID = 6618520341
    #dimonID = 
    #users = []
    #users.append(kirilID)
    #users.append(dimonID)
    
    
    #function of manually subscribing users by admin replying to their messages
    #probably FSM is also needed
    
    pinnedMessageinfo = await find_pinned_message(message, bot)
    if pinnedMessageinfo:
        if str(kirilID) in pinnedMessageinfo.text:
            return   
        else: 
            new_text = f"{pinnedMessageinfo.text}\nname:Kiril Panchul, id:{kirilID}"
        await bot.edit_message_text(chat_id=CHAT_ID, message_id=pinnedMessageinfo.message_id, text=new_text, parse_mode='HTML')
    

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
    