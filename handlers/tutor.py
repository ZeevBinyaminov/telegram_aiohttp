from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from database.database import db
from keyboards.inline import get_themes_keyboard, get_tasks_keyboard
from loader import dp


class FSMContest(StatesGroup):
    theme = State()
    difficulty = State()


@dp.message_handler(commands=['create_contest'], state=None)
async def create_contest(message: types.Message):
    await message.answer("Выберите тему контеста",
                         reply_markup=get_themes_keyboard(db.get_all_themes()))
    await FSMContest.theme.set()


@dp.callback_query_handler(state=FSMContest.theme)
async def choose_theme(callback: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['theme'] = callback.data
    await callback.message.answer("Введите сложность заданий")
    await FSMContest.next()


# @dp.message_handler(state=FSMContest.theme)
# async def get_theme(message: types.Message, state: FSMContext):
#     async with state.proxy() as data:
#         data['theme'] = message.text.strip()
#     await message.answer("Введите сложность заданий")
#     await FSMContest.next()


@dp.message_handler(state=FSMContest.difficulty)
async def get_difficulty(message: types.Message, state: FSMContext):
    if not message.text.isnumeric():
        await message.answer("Неправильный формат сложности, введите число")
        return

    async with state.proxy() as data:
        data['difficulty'] = int(message.text)
        contest = db.get_contest(*data.values())
        await message.answer("Вот Ваш контест", reply_markup=get_tasks_keyboard(contest))
        await state.finish()


@dp.callback_query_handler()
async def get_info_by_task(callback: types.CallbackQuery):
    await callback.message.answer(db.get_task_info(callback.data))

