import asyncio
import logging
from aiogram import Bot, Dispatcher
from core.settings import settings
from core.handlers.basic import router
from database.models import async_main
from core.utils.commands import set_commands

bot = Bot(token=settings.bots.bot_token)
dp = Dispatcher()


# Инициализация логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


async def start():
    dp.include_router(router)

    try:
        await set_commands(bot)
        await async_main()
        await bot.get_me()  # Проверка, работает ли бот
        logging.info('Бот работает!')
        await dp.start_polling(bot)  # Передаём объект бота для запуска опроса
    except Exception as e:
        logging.error(f'Произошла ошибка: {e}')
        await bot.send_message('712481558', f'Произошла ошибка - {e}. Бот отключился!')
    finally:
        await bot.session.close()


if __name__ == '__main__':
    try:
        asyncio.run(start())
    except KeyboardInterrupt:
        print('Бот отключен!')

