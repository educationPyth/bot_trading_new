from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault


async def set_commands(bot: Bot):
    commands = [
        BotCommand(
            command='start',
            description='Start bot'
        ),
        # BotCommand(
        #     command='help',
        #     description='helper'
        # ),
        BotCommand(
            command='start_settings',
            description='create new params for bot'
        ),
        BotCommand(
            command='menu',
            description='menu list'
        )
    ]

    await bot.set_my_commands(commands, BotCommandScopeDefault())

