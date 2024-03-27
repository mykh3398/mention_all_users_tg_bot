from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault
#from handlers.users import userCommandNamesGet, userCommandNamesPost

async def set_commands(bot: Bot):
    commands = [
        BotCommand(
            command='start',
            description="Start"
        ),
        BotCommand(
            command='hi',
            description="Say hi"
        ),
        BotCommand(
            command='subscribe',
            description="Subscribe to get notificated"
        ),
        BotCommand(
            command='all',
            description="Mention all users"
        ),
        BotCommand(
            command='create_subscription',
            description="Create new selfmade subscription"
        ),
    ]
    
    # for userCommandNameGet in userCommandNamesGet:
    #     commands.append(BotCommand(
    #         command=f"subscribe_{userCommandNameGet}",
    #         description=f"Subscription for{userCommandNameGet}"
    #     ))
        
    # for userCommandNamePost in userCommandNamesPost:
    #     commands.append(BotCommand(
    #         command=f"all_{userCommandNamesPost}",
    #         description=f"Mention all for{userCommandNamesPost}"
    #     ))
        
    await bot.set_my_commands(commands, BotCommandScopeDefault())