from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart

from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

router_u = Router()

import keyboards as kb
from requests import is_user_registered_db, save_user_to_db, get_user_data

class AddNewUser(StatesGroup):
    kurs = State()
    direction = State()
    group = State()
    telegram_id = State()

@router_u.message(CommandStart())
async def Cmd_start(message: Message):
    await message.answer(f'Привет 👋🏼,\nЯ - чат-бот \n\n'
                             f'Я могу показать: \n\n'
                             f'• \n\n')
    await message.answer(f'🔮 Главное меню', reply_markup=await kb.menu())

@router_u.message(F.text == '📌 Регистрация')
async def Cmd_register(message: Message, state: FSMContext) -> None: 
    user_id = message.from_user.id
    if await is_user_registered_db(user_id):
        await message.answer("Вы уже зарегистрированы.")
    else:
        await message.answer("Выберете свой курс", reply_markup=await kb.kurs_registration())
        
@router_u.callback_query(F.data.startswith("reg.kurs.number_"))
async def Process_kurs(query: CallbackQuery, state: FSMContext):

    kurs = int(query.data.split("_")[1])
    await query.message.answer(f'Kurs - {kurs}')
    
    await state.update_data(kurs=kurs)
    
    await query.message.answer("Выберете своё направление", reply_markup=await kb.kurs_registration())

@router_u.message(AddNewUser.fio_klient)
async def process_fio(message: Message, state: FSMContext) -> None:
    await state.update_data(fio_klient=message.text)
    await message.answer("Теперь введите ваш адрес.")
    await state.set_state(AddNewUser.adress)

@router_u.message(AddNewUser.adress)
async def process_address(message: Message, state: FSMContext) -> None:
    await state.update_data(address=message.text)
    await message.answer("Теперь введите ваш номер телефона цифрами")
    await state.set_state(AddNewUser.phone_number)

@router_u.message(AddNewUser.phone_number)
async def process_phone(message: Message, state: FSMContext) -> None:
    await state.update_data(phone_number=message.text)
    data = await state.get_data()
    message_text = (
        f"Спасибо за регистрацию!\n\n"
        f"Паспорт: <b>{data['passport']}</b>\n"
        f"ФИО: <b>{data['fio_klient']}</b>\n"
        f"Адрес: <b>{data['address']}</b>\n"
        f"Номер телефона: <b>{data['phone_number']}</b>\n\n"
        f"Если все верно, нажмите на кнопку снизу")
    await message.answer(message_text, reply_markup=await kb.register_user())

@router_u.callback_query(F.data.startswith("register"))
async def register_user(query: CallbackQuery, state: FSMContext):
    user_id = query.from_user.id
    data = await state.get_data()
    await save_user_to_db(query.from_user.id, data)
    await state.clear()
    await query.message.answer("Регистрация завершена. Спасибо за регистрацию!")
    await query.message.answer("🔮 Главное меню", reply_markup=await kb.menu(user_id, is_user_registered_db))
    
@router_u.message(F.text == '📋 Моя анкета')
async def view_profile(message: Message):
    user_id = message.from_user.id
    user_data = await get_user_data(user_id)
    if user_data:
        profile_text = (
            f"📋 Ваша анкета:\n\n"
            f"Паспорт: <b>{user_data.passport}</b>\n"
        )
        await message.answer(profile_text, reply_markup=await kb.menu(user_id))
    else:
        await message.answer("Ваша анкета не найдена. Возможно, вы еще не зарегистрированы.")