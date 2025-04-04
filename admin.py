from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

import keyboards as kb
from requests import is_admin, add_admin, get_users_by_course, get_students_by_course_and_speciality, get_users_by_group_id

router_a = Router()

class TextForKurs(StatesGroup):
    kurs = State()
    text = State()

class TextForPotok(StatesGroup):
    kurs = State()
    potok_id = State()
    text = State()

class TextForGroup(StatesGroup):
    kurs = State()
    potok_id = State()
    group_id = State()
    text = State()

class AddAdmin(StatesGroup):
    telegram_id = State()

# Работа для написания текста Курсу
@router_a.message(F.text == '📖 Курс')
async def Kurs(message: Message, state: FSMContext):
    user_id = message.from_user.id
    if await is_admin(user_id):
        await message.answer(f'Выберите курс которому вы бы хотели написать', reply_markup=await kb.kurs())
    else:
        await message.answer("У вас нет прав на выполнение этой команды.")

@router_a.callback_query(F.data.startswith("kurs.number_"))
async def Kurs_bottons_act(query: CallbackQuery, state: FSMContext):
    kurs_id = int(query.data.split("_")[1])
    await state.update_data(kurs=kurs_id)
    await query.message.answer(f'Введите сообщение для Курса')
    await state.set_state(TextForKurs.text)

@router_a.message(TextForKurs.text)
async def Kurs_text_act(message: Message, state: FSMContext):
    await state.update_data(text=message.text)
    data = await state.get_data()
    kurs_id = data["kurs"]
    await message.answer(data["text"], reply_markup=await kb.ready_kurs(kurs_id))

@router_a.callback_query(F.data.startswith("kurs.ready_"))
async def Kurs_ready_act(query: CallbackQuery, state: FSMContext):
    kurs_id = int(query.data.split("_")[1])
    data = await state.get_data()
    message_text = data["text"]
    users = await get_users_by_course(kurs_id)
    if users:
        for user in users:
            await send_message_to_user(query.bot, user.telegram_id, message_text) # Передаем query.bot
        await query.message.answer("Сообщение успешно отправлено всем пользователям курса")
    else:
        await query.message.answer("На выбранный курс не подписан ни один пользователь")
    await state.clear()

# Работа для написания текста Потоку
@router_a.message(F.text == '🎓 Поток')
async def Potok(message: Message, state: FSMContext):
    user_id = message.from_user.id
    if await is_admin(user_id):
        await message.answer(f'Чтобы выбрать поток, выберите курс', reply_markup=await kb.potok_kurs())
    else:
        await message.answer("У вас нет прав на выполнение этой команды.")

@router_a.callback_query(F.data.startswith("potok.kurs.number_"))
async def Potok_bottons_act(query: CallbackQuery, state: FSMContext):
    kurs_id = int(query.data.split("_")[1])
    await state.update_data(kurs=kurs_id)
    await query.message.answer(f'Выберете поток', reply_markup=await kb.speciality_for_curs(kurs_id))

@router_a.callback_query(F.data.startswith("potok.speciality_"))
async def Potok_text_act(query: CallbackQuery, state: FSMContext):
    speciality_id = int(query.data.split("_")[1])
    await state.update_data(potok_id=speciality_id)
    await query.message.answer(f'Введите сообщение для Потока')
    await state.set_state(TextForPotok.text)

@router_a.message(TextForPotok.text)
async def Kurs_text_act(message: Message, state: FSMContext):
    await state.update_data(text=message.text)
    data = await state.get_data()
    potok_id = data["potok_id"]
    await message.answer(data['text'], reply_markup=await kb.ready_speciality(potok_id))

@router_a.callback_query(F.data.startswith("potok.ready_"))
async def Potok_ready_act(query: CallbackQuery, state: FSMContext):
    potok_id = int(query.data.split("_")[1])
    data = await state.get_data()
    message_text = data["text"]
    course_id = data["kurs"]
    users = await get_students_by_course_and_speciality(course_id, potok_id)
    if users:
        for user in users:
            await send_message_to_user(query.bot, user.telegram_id, message_text) # Передаем query.bot
        await query.message.answer("Сообщение успешно отправлено всем пользователям потока")
    else:
        await query.message.answer("На выбранный курс не подписан ни один пользователь")
    await state.clear()

# Работа для написания текста Группе
@router_a.message(F.text == '📚 Группа')
async def Group(message: Message, state: FSMContext):
    user_id = message.from_user.id
    if await is_admin(user_id):
        await message.answer(f'Чтобы выбрать группу, выберите курс', reply_markup=await kb.kurs_group())
    else:
        await message.answer("У вас нет прав на выполнение этой команды.")

@router_a.callback_query(F.data.startswith("group.number_"))
async def Group_bottons_act(query: CallbackQuery, state: FSMContext):
    kurs_id = int(query.data.split("_")[1])
    await state.update_data(kurs=kurs_id)
    await query.message.answer(f'Выберете поток', reply_markup=await kb.group_speciality_for_curs(kurs_id))

@router_a.callback_query(F.data.startswith("group.speciality_"))
async def Group_2bot_act(query: CallbackQuery, state: FSMContext):
    speciality_id = query.data.split("_")[1]
    await state.update_data(potok_id=speciality_id)
    data = await state.get_data()
    kurs = data["kurs"]
    await query.message.answer(f'Выберете группу', reply_markup=await kb.generate_group_keyboard(kurs, speciality_id))

@router_a.callback_query(F.data.startswith("group.group_"))
async def Group_text_act(query: CallbackQuery, state: FSMContext):
    group_id = int(query.data.split("_")[1])
    await state.update_data(group_id=group_id)
    await query.message.answer(f'Введите сообщение для Группы')
    await state.set_state(TextForGroup.text)

@router_a.message(TextForGroup.text)
async def Group_text_do(message: Message, state: FSMContext):
    await state.update_data(text=message.text)
    data = await state.get_data()
    group_id = data["group_id"]
    await message.answer(data['text'], reply_markup=await kb.ready_group(group_id))

@router_a.callback_query(F.data.startswith("group.ready_"))
async def Group_ready_act(query: CallbackQuery, state: FSMContext):
    group_id = int(query.data.split("_")[1])
    data = await state.get_data()
    message_text = data["text"]
    users = await get_users_by_group_id(group_id)
    if users:
        for user in users:
            await send_message_to_user(query.bot, user.telegram_id, message_text)
        await query.message.answer("Сообщение успешно отправлено всем пользователям группы")
    else:
        await query.message.answer("На выбранный курс не подписан ни один пользователь")
    await state.clear()

# Функция отправки сообщения пользователю
async def send_message_to_user(bot: Bot, user_id, message_text):
    try:
        await bot.send_message(user_id, message_text)
        return True
    except Exception as e:
        print(f"Не удалось отправить сообщение пользователю с ID {user_id}: {e}")
        return False

# Добавление нового администратора
@router_a.message(F.text == ' Добавление нового администратора')
async def Admin(message: Message, state: FSMContext):
    user_id = message.from_user.id
    if await is_admin(user_id):
        await message.answer(f'Чтобы добавить администратора, нужен телеграмм id\n\nУзнать телеграмм id пользователя можно через бота @userinfobot\n\nДалее - отравьте 9-10 символов id аккаунта')
        await state.set_state(AddAdmin.telegram_id)
    else:
        await message.answer("У вас нет прав на выполнение этой команды.")

@router_a.message(AddAdmin.telegram_id)
async def Add_admin(message: Message, state: FSMContext):
    telegram_id = message.text
    if int(len(telegram_id)) == 9 or int(len(telegram_id)) == 10:
        result = await add_admin(telegram_id)
        if result:
            await message.answer(f"Новый администратор успешно добавлен в базу данных", reply_markup=await kb.menu_a())
        else:
            await message.answer(f"Администратор с таким Telegram ID уже существует", reply_markup=await kb.menu_a())
    else:
        await message.answer(f"Ошибка при добавлении администратора", reply_markup=await kb.menu_a())