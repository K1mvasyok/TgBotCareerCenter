from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

from requests import is_user_registered_db, get_specialities, get_groups_by_course_and_speciality, get_specialities_by_course_id, get_groups_by_course

async def menu_a():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📖 Курс"), KeyboardButton(text="🎓 Поток ")],
            [KeyboardButton(text="📚 Группа")],
            [KeyboardButton(text="📌 Добавление нового администратора")]],
        resize_keyboard=True, input_field_placeholder="Выберите пункт ниже")

async def menu_u(user_id):
    is_user_registered = await is_user_registered_db(user_id)
    registration_button = [KeyboardButton(text="📌 Регистрация")] if not is_user_registered else []
    profile_button = [KeyboardButton(text="📋 Моя анкета")] if is_user_registered else []
    return ReplyKeyboardMarkup(keyboard=[registration_button + profile_button], resize_keyboard=True, input_field_placeholder="Выберите пункт ниже")

# Клавиатура для возврата в меню
async def return_to_menu():
    return InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="🏡 Вернуться в меню", callback_data="return_to_menu")]])

# Клавиаутры для регистрации пользователя
async def kurs_registration():
    buttons = [
        [InlineKeyboardButton(text="1 Курс", callback_data=f"reg.kurs.number_1"),
         InlineKeyboardButton(text="2 Курс", callback_data=f"reg.kurs.number_2"),],
        [InlineKeyboardButton(text="3 Курс", callback_data=f"reg.kurs.number_3"),
         InlineKeyboardButton(text="4 Курс", callback_data=f"reg.kurs.number_4")],
        [InlineKeyboardButton(text="🏡 Вернуться в меню", callback_data="return_to_menu")]]
    return InlineKeyboardMarkup(inline_keyboard=buttons)

async def group_without_speciality(course_id):
    groups = await get_groups_by_course(course_id)
    keyboard = []
    row = []
    for group in groups:
        button = InlineKeyboardButton(text=group.name, callback_data=f'reg.group_{group.id}')
        row.append(button)
        if len(row) == 2:
            keyboard.append(row)
            row = []
    if row:
        keyboard.append(row)
    keyboard.append([InlineKeyboardButton(text="🏡 Вернуться в меню", callback_data="return_to_menu")])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

async def newregistration(telegram_id):
    keyboard = [[InlineKeyboardButton(text=f'Пройти регистрацию заново', callback_data=f'reg.new_{telegram_id}')]]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

# Клавиатуры для выбора курса (админ)
async def kurs():
    buttons = [
        [InlineKeyboardButton(text="1 Курс", callback_data=f"kurs.number_1"),
         InlineKeyboardButton(text="2 Курс", callback_data=f"kurs.number_2"),],
        [InlineKeyboardButton(text="3 Курс", callback_data=f"kurs.number_3"),
         InlineKeyboardButton(text="4 Курс", callback_data=f"kurs.number_4")],
        [InlineKeyboardButton(text="🏡 Вернуться в меню", callback_data="return_to_menu")]]
    return InlineKeyboardMarkup(inline_keyboard=buttons)

async def ready_kurs(kurs_id):
    keyboard = [[InlineKeyboardButton(text="✅ Готово", callback_data=f"kurs.ready_{kurs_id}")],
                [InlineKeyboardButton(text="↩️ Написать еще раз", callback_data=f"kurs.number_{kurs_id}")],
                [InlineKeyboardButton(text="🏡 Вернуться в меню", callback_data="return_to_menu")]]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

# Клавиатурs для потока (админ)
async def potok_kurs():
    buttons = [
        [InlineKeyboardButton(text="1 Курс", callback_data=f"potok.kurs.number_1"),
         InlineKeyboardButton(text="2 Курс", callback_data=f"potok.kurs.number_2"),],
        [InlineKeyboardButton(text="3 Курс", callback_data=f"potok.kurs.number_3"),
         InlineKeyboardButton(text="4 Курс", callback_data=f"potok.kurs.number_4")],
        [InlineKeyboardButton(text="🏡 Вернуться в меню", callback_data="return_to_menu")]]
    return InlineKeyboardMarkup(inline_keyboard=buttons)

async def speciality_for_curs(course_id):
    speciality = await get_specialities_by_course_id(course_id)
    keyboard = [[InlineKeyboardButton(text=speciality.name, callback_data=f'potok.speciality_{speciality.id}')] for speciality in speciality]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

async def ready_speciality(speciality_id):
    keyboard = [[InlineKeyboardButton(text="✅ Готово", callback_data=f"potok.ready_{speciality_id}")],
                [InlineKeyboardButton(text="↩️ Написать еще раз", callback_data=f"potok.speciality_{speciality_id}")],
                [InlineKeyboardButton(text="🏡 Вернуться в меню", callback_data="return_to_menu")]]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

# Клавиатуры для группы (админ)
async def kurs_group():
    buttons = [
        [InlineKeyboardButton(text="1 Курс", callback_data=f"group.number_1"),
         InlineKeyboardButton(text="2 Курс", callback_data=f"group.number_2"),],
        [InlineKeyboardButton(text="3 Курс", callback_data=f"group.number_3"),
         InlineKeyboardButton(text="4 Курс", callback_data=f"group.number_4")],
        [InlineKeyboardButton(text="🏡 Вернуться в меню", callback_data="return_to_menu")]]
    return InlineKeyboardMarkup(inline_keyboard=buttons)

async def group_speciality_for_curs(course_id):
    speciality = await get_specialities_by_course_id(course_id)
    keyboard = [[InlineKeyboardButton(text=speciality.name, callback_data=f'group.speciality_{speciality.id}')] for speciality in speciality]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

async def generate_group_keyboard(course_id, speciality_id):
    group = await get_groups_by_course_and_speciality(course_id, speciality_id)
    keyboard = [[InlineKeyboardButton(text=group.name, callback_data=f"group.group_{group.id}")] for group in group]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

async def ready_group(group_id):
    keyboard = [[InlineKeyboardButton(text="✅ Готово", callback_data=f"group.ready_{group_id}")],
                [InlineKeyboardButton(text="↩️ Написать еще раз", callback_data=f"group.group_{group_id}")],
                [InlineKeyboardButton(text="🏡 Вернуться в меню", callback_data="return_to_menu")]]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)