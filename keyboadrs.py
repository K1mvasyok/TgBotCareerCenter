from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton


async def menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📖 "), KeyboardButton(text="📚 ")],
            [KeyboardButton(text="🎓 "), KeyboardButton(text="📅 ")],], 
        resize_keyboard=True, input_field_placeholder="Выберите пункт ниже")
    
# Клавиатура для возврата в меню
async def return_to_menu():
    return InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="🏡 Вернуться в меню", callback_data="return_to_menu")]])
    
# Клавиатура со списком потоков 
async def groups_by_potok():
    airlines = await get_groups()
    keyboard = [[InlineKeyboardButton(text=groups.name, callback_data=f'group:{group.id}')] for group in groups]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)
