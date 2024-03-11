from aiogram import F, Router
from aiogram.types import Message
from aiogram.filters import CommandStart

router = Router()

import keyboards as kb

@router.message(CommandStart())
async def Cmd_start(message: Message):
    await message.answer(f'Привет 👋🏼,\nЯ - чат-бот \n\n'
                             f'Я могу показать: \n\n'
                             f'• \n\n')
    await message.answer(f'🔮 Главное меню', reply_markup=await kb.menu())

# Обработка кнопки "Написать потоку"
@router.message(F.text == '📖 Поток')
async def Potok(message: Message):
    await message.answer(f'Выберите поток, чтобы написать сообщение для него:', reply_markup=await kb.menu())

# Обработка нажатия на поток
@router_u.callback_query(F.data.startswith("potok_id:"))
async def Show_potok(query: types.CallbackQuery):
    potok = int(query.data.split(":")[1])
    disciplines = await get_disciplines_by_semester(semester) 
