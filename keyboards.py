from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton


async def menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📖 Поток"), KeyboardButton(text="📚 ")],
            [KeyboardButton(text="🎓 "), KeyboardButton(text="📅 ")],], 
        resize_keyboard=True, input_field_placeholder="Выберите пункт ниже")
    
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