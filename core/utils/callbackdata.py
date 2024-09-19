from aiogram.fsm.state import State, StatesGroup


class UserChannel(StatesGroup):
    chat = State()
    contract = State()
    photo = State()
    links = State()


class UserEditChannel(StatesGroup):
    photo = State()
    links = State()


class RemoveChannel(StatesGroup):
    name_channel = State()