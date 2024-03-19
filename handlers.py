from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart

router_u = Router()

import keyboards as kb

@router_u.message(CommandStart())
async def Cmd_start(message: Message):
    await message.answer(f'Привет 👋🏼,\nЯ - чат-бот \n\n'
                             f'Я могу показать: \n\n'
                             f'• \n\n')
    await message.answer(f'🔮 Главное меню', reply_markup=await kb.menu())

# Обработка кнопки "Написать потоку"
@router_u.message(F.text == '📖 Поток')
async def Potok(message: Message):
    await message.answer(f'Выберите поток, чтобы написать сообщение для него:', reply_markup=await kb.menu())

# Обработка нажатия на поток
@router_u.callback_query(F.data.startswith("potok_id:"))
async def Show_potok(query: CallbackQuery):
    potok = int(query.data.split(":")[1])