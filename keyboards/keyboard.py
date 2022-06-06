from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


parse_false = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True).add(*['/add', '/delete', '/info', '/parse'])
parse_true = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True).add(*['/add', '/delete', '/info', '/stop'])
delete_inline = InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton(text='удалить', callback_data='delete'))
