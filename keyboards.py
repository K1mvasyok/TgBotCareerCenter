from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

from requests import is_user_registered_db, get_direction, get_groups_by_course_and_direction

async def menu_a():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📖 Курс"), KeyboardButton(text="📚 ")],
            [KeyboardButton(text="🎓 "), KeyboardButton(text="📅 ")],], 
        resize_keyboard=True, input_field_placeholder="Выберите пункт ниже")

async def menu_u(user_id):
    is_user_registered = await is_user_registered_db(user_id)
    registration_button = [KeyboardButton(text="📌 Регистрация")] if not is_user_registered else []
    profile_button = [KeyboardButton(text="📋 Моя анкета")] if is_user_registered else []
    return ReplyKeyboardMarkup(keyboard=[registration_button + profile_button], resize_keyboard=True, input_field_placeholder="Выберите пункт ниже")

# Клавиатура для возврата в меню
async def return_to_menu():
    return InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="🏡 Вернуться в меню", callback_data="return_to_menu")]])
    
# Клавиатура для выбора курса для курса
async def kurs():
    buttons = [
        [InlineKeyboardButton(text="1 Курс", callback_data=f"kurs.number_1"),
        InlineKeyboardButton(text="2 Курс", callback_data=f"kurs.number_2"),],
        [InlineKeyboardButton(text="3 Курс", callback_data=f"kurs.number_3"),
        InlineKeyboardButton(text="4 Курс", callback_data=f"kurs.number_4")],
        [InlineKeyboardButton(text="🏡 Вернуться в меню", callback_data="return_to_menu")]]
    return InlineKeyboardMarkup(inline_keyboard=buttons)
    
async def kurs_registration():
    buttons = [
        [InlineKeyboardButton(text="1 Курс", callback_data=f"reg.kurs.number_1"),
        InlineKeyboardButton(text="2 Курс", callback_data=f"reg.kurs.number_2"),],
        [InlineKeyboardButton(text="3 Курс", callback_data=f"reg.kurs.number_3"),
        InlineKeyboardButton(text="4 Курс", callback_data=f"reg.kurs.number_4")],
        [InlineKeyboardButton(text="🏡 Вернуться в меню", callback_data="return_to_menu")]]
    return InlineKeyboardMarkup(inline_keyboard=buttons)

async def directions():
    direction = await get_direction()
    keyboard = [[InlineKeyboardButton(text=direction.name, callback_data=f'reg.direction_{direction.id}')] for direction in direction]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

async def group(course_id, direction_id):
    group = await get_groups_by_course_and_direction(course_id, direction_id)
    keyboard = [[InlineKeyboardButton(text=group.name, callback_data=f'reg.group_{group.id}')] for group in group]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

async def ready(kurs_id):
    keyboard = [[InlineKeyboardButton(text="✅ Готово", callback_data=f"kurs.ready_{kurs_id}")],
                [InlineKeyboardButton(text="↩️ Написать еще раз", callback_data=f"kurs.number_{kurs_id}")]]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)