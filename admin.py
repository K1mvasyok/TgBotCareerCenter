from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command

import keyboards as kb
from config import ADMIN_TELEGRAM_ID

router_a = Router()

@router_a.message(Command("commands"))
async def Cmd_start(message: Message):
    if message.from_user.id == ADMIN_TELEGRAM_ID:
        await message.answer(f'Привет 👋🏼,\nЯ - чат-бот \n\n'
                             f'Через меня можно написать ?сообщение?: \n\n'
                             f'• Курсу\n\n'
                             f'• Потоку\n\n'
                             f'• Или конкретной группе\n\n')
        await message.answer(f'🔮 Главное меню', reply_markup=await kb.menu())
    else:
        await message.answer("У вас нет прав на выполнение этой команды.")

# Работа для написания текста Курсу
@router_a.message(F.text == '📖 Курс')
async def Kurs(message: Message):
    if message.from_user.id == ADMIN_TELEGRAM_ID:
        await message.answer(f'Выберите курс которому вы бы хотели написать', reply_markup=await kb.kurs())  
    else:
        await message.answer("У вас нет прав на выполнение этой команды.")

@router_a.callback_query(F.data.startswith("kurs.number"))
async def Kyrs_bottons_act(query: CallbackQuery):
    kurs = int(query.data.split("_")[1])
    await query.message.answer(f'Kurs - {kurs}')
    
    
# Работа для написания текста Потоку
# План: Кнопка-Хэдлер


# Работа для написания текста Группе