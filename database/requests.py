from database.models import async_session
from database.models import User, UserBot
from sqlalchemy import select, update, delete


async def set_user(tg_id):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))

        if not user:
            session.add(User(tg_id=tg_id))
            await session.commit()


async def set_data(tg_id, chat, contract, photo, links, title_channel, transactions_time):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        user_bot = UserBot(chat=chat, contract=contract, photo=photo, links=links, owner_id=user.id, title_channel=title_channel, transactions_time=transactions_time)
        session.add(user_bot)
        await session.commit()
        # if user:
        #     user_bot = UserBot(chat=chat, contract=contract, photo=photo, links=links, owner_id=user.id, title_channel=title_channel, transactions_time=transactions_time)
        #     session.add(user_bot)
        #     await session.commit()
        # else:
        #     # Если пользователь не существует, то создаем его.
        #     new_user = User(tg_id=tg_id)
        #     session.add(new_user)
        #     await session.commit()
        #
        #     # Теперь добавляем UserBot
        #     user_bot = UserBot(chat=chat, contract=contract, photo=photo, links=links, owner=new_user.id, title_channel=title_channel, transactions_time=transactions_time)
        #     session.add(user_bot)
        #     await session.commit()


async def get_data(tg_id):
    async with async_session() as session:
        # Запрашиваем пользователя по tg_id
        result = await session.execute(select(User).filter(User.tg_id == tg_id))
        user = result.scalar_one_or_none()  # Получаем пользователя или None

        if user:
            # Пользователь найден, теперь запрашиваем его боты
            bots_result = await session.execute(
                select(UserBot).filter(UserBot.owner_id == user.id))  # Используем user.id
            bots = bots_result.scalars().all()  # Получаем всех ботов пользователя

            data = {
                'bots': [{
                    'id': bot.id,
                    'chat': bot.chat,
                    'title_channel': bot.title_channel,
                    'contract': bot.contract,
                    'photo': bot.photo,
                    'links': bot.links,
                    'transactions_time': bot.transactions_time} for bot in bots]
            }
            return data
        else:
            return None  # Пользователь с таким tg_id не найден


async def delete_data(bot_id):
    async with async_session() as session:
        # Запрашиваем бота по bot_id
        bot = await session.scalar(select(UserBot).where(UserBot.id == bot_id))
        await session.delete(bot)
        await session.commit()


async def check_chat(chat):
    async with async_session() as session:
        chat = await session.scalar(select(UserBot).where(UserBot.chat == chat))
        return chat


async def set_last_time_transaction(last_time_transactions, chat_id):
    async with async_session() as session:
        # Получаем объект UserBot по chat_id
        chat = await session.scalar(select(UserBot).where(UserBot.chat == chat_id))

        if chat:  # Проверяем, найден ли объект
            chat.transactions_time = last_time_transactions  # Обновляем поле
            await session.commit()  # Сохраняем изменения
        else:
            print("Chat not found")  # Обработка случая, когда чат не найден


async def bot_id(chat):
    async with async_session() as session:
        bot = await session.scalar(select(UserBot).where(UserBot.chat == chat))
        return bot

