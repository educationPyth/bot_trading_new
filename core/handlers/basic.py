import asyncio

from aiogram import Bot
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram import F, Router

from core.parser.handler_parser import check_transactions
from core.utils.callbackdata import UserChannel, UserEditChannel, RemoveChannel
import core.keyboards.inline as kb
import database.requests as rq


router = Router()


@router.message(Command('start'))
async def get_start(message: Message, bot: Bot):
    user_id = message.from_user.id
    await rq.set_user(user_id)
    await bot.send_message(user_id,f'Привет {message.from_user.first_name}\n'
                                   f'Перейдите в группу или л/c, где должен работать бот.\n'
                                   f'\n'
                                   f'Дайте боту права Администратора 🔐\n'
                                   f'Затем пропишите команду /start_settings и следуйте инструкции', parse_mode='HTML')


@router.message(Command('start_settings'))
async def start_settings(message: Message, state: FSMContext):
    await message.answer('Выберите пункты для настройки:', reply_markup=await kb.menu())


@router.message(Command('menu'))
async def view_menu(message: Message):
    await message.answer('Выберите пункты для настройки:', reply_markup=await kb.menu())


@router.callback_query(F.data == 'create_bot')
async def create_bot(callback: CallbackQuery, state: FSMContext):
    chat_id = callback.message.chat.id
    active_chat = await rq.check_chat(chat_id)
    await callback.answer()

    if active_chat:
        await callback.message.answer('❌❌В этом чат-канале уже работает бот.❌❌\n\n'
                             'Попробуйте команду /start_settings в другом чат-канале.\n'
                             'Предварительно дав права администратора боту', reply_markup=await kb.home())
    else:
        await state.update_data(chat=chat_id)
        await state.update_data(title_channel=callback.message.chat.title)
        await callback.message.edit_text('Передайте нужные поля\n\n'
                                         '* - обязательное поле:', reply_markup=await kb.settings_create())


@router.callback_query(F.data == 'home')
async def get_back(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text('ВЫберите пункты для настройки:', reply_markup=await kb.menu())


@router.callback_query(F.data == 'contract')
async def get_contract(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.answer('Введите контракт c coinmarketcap (‼️‼️  ️contract pair ‼️‼️)\n'
                                  'Основной контракт не подойдет.')
    await state.set_state(UserChannel.contract)


@router.message(UserChannel.contract)
async def step_contract(message: Message, state: FSMContext):
    await state.update_data(contract=message.text)
    chat_id = message.chat.id
    await state.update_data(chat=chat_id)
    await state.update_data(title_channel=message.chat.title)
    await message.answer('Контракт получен! Если необходимо добавьте картинку и ссылки', reply_markup=await kb.settings_add() )


@router.callback_query(F.data == 'photo')
async def get_photo(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.edit_text('Вставьте фото!')
    await state.set_state(UserChannel.photo)


@router.message(UserChannel.photo)
async def step_photo(message: Message, state: FSMContext):
    if message.photo:
        await state.update_data(photo=message.photo[-1].file_id)
        await message.answer('Отлично, картинка получена.', reply_markup=await kb.settings_add())
    else:
        await message.answer('❌❌Неверный формат, вставьте только картинку.❌❌')


@router.callback_query(F.data == 'links')
async def get_links(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.edit_text('Вставьте ссылки через пробел')
    await state.set_state(UserChannel.links)


@router.message(UserChannel.links)
async def step_links(message: Message, state: FSMContext):
    if message.text:
        await state.update_data(links=message.text)
        await message.answer('Ссылки сохранены.', reply_markup=await kb.settings_add())
    else:
        await message.answer('Ссылки должны быть текстом, через пробел')


@router.callback_query(F.data == 'finish_state')
async def finish_state(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    await callback.answer()
    data = await state.get_data()

    if 'contract' in data:

        contract = data['contract']
        chat = data['chat']
        transactions_time = 0
        title_channel = data['title_channel']
        if title_channel is None:
            title_channel = 'Закрытая группа'
        photo_id = data.get('photo', '')
        links = data.get('links', '')


        # Формируем сообщение с учётом возможных пустых значений
        response_text = (f'✅✅Ваши данные успешно сохранены✅✅\n'
                         f'Контракт: {data["contract"]}\n'
                         f'Картинка: {photo_id if photo_id else "Нет"}\n'
                         f'Ссылки: {links if links else "Нет"}\n'
                         f'Чат: {chat}\n'
                         f'Название канала: {title_channel}\n\n'
                         f'Чтобы начать использовать введите /startbot ▶️')

        await callback.message.answer(response_text, reply_markup=await kb.home())
        await rq.set_data(tg_id=user_id, chat=chat, contract=contract, photo=photo_id, links=links, title_channel=title_channel, transactions_time=transactions_time)
        await state.clear()

    else:
        await callback.message.answer('‼️Поле контракт обязательно для заполнения!‼️', reply_markup=await kb.settings_add())


@router.callback_query(F.data == 'my_bots')
async def view_my_bots(callback: CallbackQuery):
    user_id = callback.from_user.id  # tg_id
    data = await rq.get_data(user_id)

    await callback.answer()
    if data['bots']:
        await callback.message.answer(f'Нажмите, чтобы выбрать действие.\n\n'
                                      f'Список подключенных каналов:\n'
                                      f'👇👇👇', reply_markup=await kb.view_channel(user_id))
    else:
        await callback.message.answer(f'У вас еще нет подключенных ботов.', reply_markup=await kb.add_bot())


@router.callback_query(F.data.startswith("name_"))
async def choose_delete_bot(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    data_button = callback.data  # например, будет 'name_1'
    bot_id = data_button.split("_")[1]  # Извлекаем ID бота, который находится после "name_"
    await state.update_data(bot_id=bot_id)
    # Здесь можно выполнить нужные действия с bot_id
    await callback.answer()
    await callback.message.answer(f'Что делаем?', reply_markup=await kb.settings_bot())
    await state.set_state(RemoveChannel.name_channel)


@router.callback_query(F.data == 'delete_bot', RemoveChannel.name_channel)
async def delete_bot(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    data_state = await state.get_data()
    bot_id = data_state.get('bot_id')

    await callback.answer()
    await rq.delete_data(bot_id)
    await callback.message.answer(f'Бот удален!✅\n\n'
                                  f'Список оставшихся подключенных каналов:👇👇👇\b', reply_markup=await kb.view_channel(user_id))


@router.callback_query(F.data == 'edit_bot')
async def edit_settings(callback: CallbackQuery, state: FSMContext):
    await callback.answer('временно не доступно..')


@router.message(F.text == '/startbot')
async def start_bot(message: Message, bot: Bot):
    await message.delete()
    user_id = message.from_user.id
    chat_id = message.chat.id
    time_delay = 30

    while True:
        data_parser = await check_transactions(user_id=user_id, chat_id=chat_id)
        await asyncio.sleep(time_delay)

        if data_parser == 'equally':
            print('equally')
            continue
        elif data_parser:
            print(type(data_parser))
            print(data_parser)
            text = data_parser['html']
            photo = data_parser['photo']

            if photo:
                await bot.send_photo(chat_id=chat_id,
                                     caption=f'{text}',
                                     photo=f'{photo}',
                                     reply_markup=await kb.user_links(f'{chat_id}'),
                                     parse_mode='HTML')
            else:
                await bot.send_message(chat_id=chat_id, text=f'{text}',reply_markup=await kb.user_links(f'{chat_id}'),  parse_mode='HTML')
        else:
            await bot.send_message(chat_id=chat_id, text='Проблемы с Coinmarketcup. Что-то пошло не так... попробуйте заменить контракт или повторить позже.')
            break




