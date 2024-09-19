from aiogram.utils.keyboard import InlineKeyboardBuilder
import database.requests as rq


async def home():
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(text='На главную 🏡', callback_data='home')
    keyboard_builder.adjust(1)
    return keyboard_builder.as_markup()


async def menu():
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(text='Создать ➡️', callback_data='create_bot')
    keyboard_builder.button(text='Подключенные каналы 📋', callback_data='my_bots')
    keyboard_builder.adjust(1)
    return keyboard_builder.as_markup()


async def settings_bot():
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(text='Редактировать 🖌', callback_data='edit_bot')
    keyboard_builder.button(text='Удалить ❌', callback_data='delete_bot')
    keyboard_builder.button(text='На главную 🏡', callback_data='home')
    keyboard_builder.adjust(1)
    return keyboard_builder.as_markup()


async def settings_create():
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(text='📄 Контракт *', callback_data='contract')
    keyboard_builder.button(text='Картинка 🖼', callback_data='photo')
    keyboard_builder.button(text='Ссылки 🔗', callback_data='links')
    keyboard_builder.button(text='На главную 🏡', callback_data='home')
    keyboard_builder.adjust(1)
    return keyboard_builder.as_markup()


async def settings_add():
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(text='Завершить 🟢', callback_data='finish_state')
    keyboard_builder.button(text='📄 Контракт *', callback_data='contract')
    keyboard_builder.button(text='Картинка 🖼', callback_data='photo')
    keyboard_builder.button(text='Ссылки 🔗', callback_data='links')
    keyboard_builder.button(text='На главную 🏡', callback_data='home')
    keyboard_builder.adjust(1)
    return keyboard_builder.as_markup()


async def view_channel(user_id):
    keyboard_builder = InlineKeyboardBuilder()
    data = await rq.get_data(user_id)

    if data:
        for bot in data['bots']:  # Перебираем список словарей в поле 'bots'
            keyboard_builder.button(text=bot['title_channel'], callback_data=f'name_{bot["id"]}')
        keyboard_builder.button(text='На главную 🏡', callback_data='home')
        return keyboard_builder.adjust(1).as_markup()


async def edit(bot_id):
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(text='Завершить 🟢', callback_data='finish_edit')
    keyboard_builder.button(text='Картинка 🖼', callback_data=f'editbot_{bot_id}_photo')
    keyboard_builder.button(text='Ссылки 🔗', callback_data=f'editbot_{bot_id}_links')
    keyboard_builder.button(text='На главную 🏡', callback_data='home')
    keyboard_builder.adjust(1)
    return keyboard_builder.as_markup()


async def add_bot():
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(text='Создать ➡️', callback_data='create_bot')
    keyboard_builder.button(text='На главную 🏡', callback_data='home')
    keyboard_builder.adjust(1)
    return keyboard_builder.as_markup()


async def user_links(chat_id):
    keyboard_builder = InlineKeyboardBuilder()
    bot_data = await rq.bot_id(chat_id)

    if bot_data and bot_data.links:
        # Разбиваем строки на список ссылок
        links = bot_data.links.split(';')

        for link in links:
            if link.strip():  # Проверка на пустую строку
                name, url = link.split(maxsplit=1)  # Разделяем на имя и ссылку
                keyboard_builder.button(text=name, url=url)

        return keyboard_builder.adjust(2).as_markup()  # Возвращаем клавиатуру

    return None  # Если данных нет, возвращаем None





