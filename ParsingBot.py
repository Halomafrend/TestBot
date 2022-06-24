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
import logging

USER_ID = [5378097032, 631390821]
storage = MemoryStorage()
bot = Bot(token=config.TOKEN)
dp = Dispatcher(bot, storage=storage)
logging.basicConfig(level=logging.INFO)

global is_trace
is_trace = False


class FSM_add(StatesGroup):
    get_link = State()


async def on_start_up(_):
    database.sql_start()


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    print(message.from_user.id)
    if message.from_user.id in USER_ID:
        await message.answer('Для добавления ссылки: "/add"\nДля удаления: "/delete"\nСписок ссылок: "/info"\nНачать парсинг: "/parse"', reply_markup=kb.parse_false)


@dp.message_handler(commands=['add'])
async def add(message: types.Message):
    if message.from_user.id in USER_ID:
        await FSM_add.get_link.set()
        await message.reply('Введи ссылку')


@dp.message_handler(state=FSM_add.get_link)
async def get_link(message: types.Message, state: FSMContext):
    await message.reply('Проверяю...')
    is_continue_out = parser.is_continue(message.text)
    if is_continue_out != 1 and is_continue_out != 0:
        await message.reply('Неверная ссылка')
        await message.reply(is_continue_out)
    else:
        await database.sql_add_command(message.text)
        await message.reply('Ссылка добавлена')
    await state.finish()


@dp.message_handler(commands=['delete'])
async def list_to_delete(message: types.Message):
    if message.from_user.id in USER_ID:
        links = await database.sql_read()
        for link in links:
            await message.answer(link[0], reply_markup=kb.delete_inline)


@dp.callback_query_handler(text='delete')
async def delete(callback: types.CallbackQuery):
    await database.sql_delete_command(callback.message.text)
    await callback.message.delete()


@dp.message_handler(commands=['info'])
async def info(message: types.Message):
    if message.from_user.id in USER_ID:
        links = await database.sql_read()
        for link in links:
            await message.answer(link[0])


@dp.message_handler(commands=['parse'])
async def trace(message: types.Message):
    if message.from_user.id in USER_ID:
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
                    for id in USER_ID:
                        await bot.send_message(id, 'Cвободно:' + link[0])
                    await database.sql_delete_command(link[0])
                elif parser.is_continue(link[0]) != 1:
                        await bot.send_message(63139082, parser.is_continue(link[0]))
                # print(link[0])
                await asyncio.sleep(1)
            await asyncio.sleep(1)



@dp.message_handler(commands=['stop'])
async def stop(message: types.Message):
    if message.from_user.id in USER_ID:
        global is_trace
        if is_trace:
            is_trace = False
            await message.answer('Парсер остановлен', reply_markup=kb.parse_false)
        else:
            await message.answer('Парсер не работает')


executor.start_polling(dp, skip_updates=True, on_startup=on_start_up)
