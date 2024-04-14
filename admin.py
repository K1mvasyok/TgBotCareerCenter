from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

import keyboards as kb
from config import ADMIN_TELEGRAM_ID
from requests import get_users_by_course
from run import get_bot

router_a = Router()

class TextForKurs(StatesGroup):
    kurs = State()
    text = State()
    
class TextForPotok(StatesGroup):
    kurs = State()
    potok_id = State()
    text = State()    

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
async def Kurs(message: Message, state: FSMContext):
    if message.from_user.id == ADMIN_TELEGRAM_ID:
        await message.answer(f'Выберите курс которому вы бы хотели написать', reply_markup=await kb.kurs())  
    else:
        await message.answer("У вас нет прав на выполнение этой команды.")

@router_a.callback_query(F.data.startswith("kurs.number_"))
async def Kurs_bottons_act(query: CallbackQuery, state: FSMContext):
    kurs_id = int(query.data.split("_")[1])
    await state.update_data(kurs=kurs_id)
    await state.set_state(TextForKurs.text)    
    await query.message.answer(f'Введите сообщение для Курса')     
    
@router_a.message(TextForKurs.text)
async def Kurs_text_act(message: Message, state: FSMContext):
    await state.update_data(text=message.text)
    data = await state.get_data()
    kurs_id = data["kurs"]    
    await message.answer(data["text"], reply_markup=await kb.ready(kurs_id))  
    
@router_a.callback_query(F.data.startswith("kurs.ready_"))
async def Kurs_ready_act(query: CallbackQuery, state: FSMContext):
    kurs_id = int(query.data.split("_")[1])
    data = await state.get_data()
    message_text = data["text"]
    users = await get_users_by_course(kurs_id)
    if users:
            for user in users:
                await send_message_to_user(user.telegram_id, message_text)
            await query.message.answer("Сообщение успешно отправлено всем пользователям курса")
    else:
            await query.message.answer("На выбранный курс не подписан ни один пользователь")
    await state.clear()

# Работа для написания текста Потоку
@router_a.message(F.text == '🎓 Поток')
async def Potok(message: Message, state: FSMContext):
    if message.from_user.id == ADMIN_TELEGRAM_ID:
        await message.answer(f'Чтобы выбрать поток, выберите курс', reply_markup=await kb.potok_kurs())  
    else:
        await message.answer("У вас нет прав на выполнение этой команды.")

@router_a.callback_query(F.data.startswith("potok.kurs.number_"))
async def Potok_bottons_act(query: CallbackQuery, state: FSMContext):
    kurs_id = int(query.data.split("_")[1])
    await state.update_data(kurs=kurs_id)        
    await query.message.answer(f'Выберете поток', reply_markup=await kb.direction_for_curs(kurs_id))          
        
# Функция отправки сообщения пользователю
async def send_message_to_user(user_id, message_text):
    bot = await get_bot()
    try:
        await bot.send_message(user_id, message_text)
        return True  
    except Exception as e:
        print(f"Не удалось отправить сообщение пользователю с ID {user_id}: {e}")
        return False   