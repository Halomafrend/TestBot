import asyncio
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils import executor
import os
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import config
from parser_dir import parser
from data_base import database
from keyboards import keyboard as kb


storage = MemoryStorage()
bot = Bot(token=config.TOKEN)
dp = Dispatcher(bot, storage=storage)


global is_trace
is_trace = False


class FSM_add(StatesGroup):
    get_link = State()


async def on_start_up(_):
    database.sql_start()


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer('Для добавления ссылки: "/add"\nДля удаления: "/delete"\nСписок ссылок: "/info"\nНачать парсинг: "/parse"', reply_markup=kb.parse_false)


@dp.message_handler(commands=['add'])
async def add(message: types.Message):
    await FSM_add.get_link.set()
    await message.reply('Введи ссылку')


@dp.message_handler(state=FSM_add.get_link)
async def get_link(message: types.Message, state: FSMContext):
    if parser.is_continue(message.text) == 2:
        await message.reply('Неверная ссылка')
    else:
        await database.sql_add_command(message.text)
        await message.reply('Ссылка добавлена')
    await state.finish()

@dp.message_handler(commands=['delete'])
async def list_to_delete(message: types.Message):
    links = await database.sql_read()
    for link in links:
        await message.answer(link[0], reply_markup=kb.delete_inline)


@dp.callback_query_handler(text='delete')
async def delete(callback: types.CallbackQuery):
    await database.sql_delete_command(callback.message.text)
    await callback.message.delete()
    # await callback.answer('Cсылка была удалена', show_alert=True)


@dp.message_handler(commands=['info'])
async def info(message: types.Message):
    links = await database.sql_read()
    for link in links:
        await message.answer(link[0])


@dp.message_handler(commands=['parse'])
async def trace(message: types.Message):
    global is_trace
    if not is_trace:
        is_trace = True
        await message.answer("Парсер запущен", reply_markup=kb.parse_true)
    else:
        await message.answer("Парсер уже запущен")

    while is_trace:
        links = await database.sql_read()
        if not links:
            await message.answer('Нет ссылок')
            await stop(message)

        for link in links:
            if parser.is_continue(link[0]) == 0:
                await bot.send_message(631390821, 'Cвободно:' + link[0])
                await database.sql_delete_command(link[0])
            # print(link[0])
            await asyncio.sleep(1)
        await asyncio.sleep(1)


# @dp.callback_query_handler(text='stop_trace')
@dp.message_handler(commands=['stop'])
async def stop(message: types.Message):
    global is_trace
    if is_trace:
        is_trace = False
        await message.answer('Парсер остановлен', reply_markup=kb.parse_false)
    else:
        await message.answer('Парсер не работает')


executor.start_polling(dp, skip_updates=True, on_startup=on_start_up)
