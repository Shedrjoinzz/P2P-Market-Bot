from aiogram import executor, types
from aiogram.utils.exceptions import NetworkError, ValidationError

import logging
import asyncio

from loader import dp, bot
from src.settings.set_commands import set_default_commands
from src.handlers import *
from src.system.middlwares_bot.anti_spam import ThrottlingMiddleware
from src.system.middlwares_bot.update_currency import while_method_update

logging.basicConfig(level=logging.INFO)


async def on_startup(dispatcher):
    asyncio.create_task(while_method_update(True))
    await set_default_commands(dispatcher)

def start_bot():
    dp.middleware.setup(ThrottlingMiddleware())
    executor.start_polling(dp, on_startup=on_startup, skip_updates=False)
    
if __name__ == "__main__":
    try:
        start_bot()
    except NetworkError:
        print('ОЩИБКА: Не удается подключиться к хосту, проверьте подключение к интернету')
    except ValidationError:
        print('Токен недействителен!\nУкажите ТОКЕН!')