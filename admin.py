from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command

import keyboards as kb
from config import ADMIN_TELEGRAM_ID

router_a = Router()

@router_a.message(Command("commands"))
async def Start_commands_for_admin(message: Message) -> None:
    if message.from_user.id == ADMIN_TELEGRAM_ID:
        await message.answer(f"Список всех доступных команд\n\n"
                             f"/kurs - \n\n"
                             f"/groups - \n\n"
                             f"/ - \n\n"
                             f"/ - \n\n")                       
    else:
        await message.answer("У вас нет прав на выполнение этой команды.")

@router_a.message(Command("kurs"))
async def Kurs(message: Message):
    if message.from_user.id == ADMIN_TELEGRAM_ID:
        await message.answer(f'Выберите курс которому вы бы хотели написать', reply_markup=await kb.kurs())  
    else:
        await message.answer("У вас нет прав на выполнение этой команды.")

@router_a.callback_query(F.data.startswith(""))
async def Airlines_inf(query: CallbackQuery):
    pass
