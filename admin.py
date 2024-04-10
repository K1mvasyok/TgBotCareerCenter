from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command

import keyboards as kb
from config import ADMIN_TELEGRAM_ID
from requests import get_users_by_course
from run import get_bot

router_a = Router()

@router_a.message(Command("commands"))
async def Cmd_commands(message: Message):
    if message.from_user.id == ADMIN_TELEGRAM_ID:
        await message.answer(f'Привет 👋🏼,\nЯ - чат-бот \n\n'
                             f'Через меня можно написать ?сообщение?: \n\n'
                             f'• Курсу\n\n'
                             f'• Потоку\n\n'
                             f'• Или конкретной группе\n\n')
        await message.answer(f'🔮 Главное меню', reply_markup=await kb.menu_a())
    else:
        await message.answer("У вас нет прав на выполнение этой команды.")

# Работа для написания текста Курсу
@router_a.message(F.text == '📖 Курс')
async def Kurs(message: Message):
    if message.from_user.id == ADMIN_TELEGRAM_ID:
        await message.answer(f'Выберите курс которому вы бы хотели написать', reply_markup=await kb.kurs())  
    else:
        await message.answer("У вас нет прав на выполнение этой команды.")

@router_a.callback_query(F.data.startswith("mes.kurs.number_"))
@router_a.callback_query(F.data.startswith("kurs.number_"))
async def Kurs_bottons_act(query: CallbackQuery):
    kurs_id = int(query.data.split("_")[1])
    await query.message.answer(f'Введите сообщение для Курса', reply_markup=await kb.ready(kurs_id))  
    
# Функция отправки сообщения пользователю
async def send_message_to_user(user_id, message_text):
    bot = await get_bot()
    try:
        await bot.send_message(user_id, message_text)
        return True  
    except Exception as e:
        print(f"Не удалось отправить сообщение пользователю с ID {user_id}: {e}")
        return False   
    
@router_a.callback_query(F.data.startswith("kurs.ready"))
async def Kurs_ready_act(query: CallbackQuery):
    kurs_id = int(query.data.split("_")[1])
    
    users = await get_users_by_course(kurs_id)
    
    if users:
            message_text = query.message.text
            await send_message_to_user(users, message_text)
            await query.message.answer("Сообщение успешно отправлено всем пользователям курса")
    else:
            await query.message.answer("На выбранный курс не подписан ни один пользователь")


# Работа для написания текста Группе