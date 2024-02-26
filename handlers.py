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