from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton


async def menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📖 "), KeyboardButton(text="📚 ")],
            [KeyboardButton(text="🎓 "), KeyboardButton(text="📅 ")],], 
        resize_keyboard=True, input_field_placeholder="Выберите пункт ниже")

@router_u.callback_query(F.data.startswith("return_to_menu"))
async def Return_to_menu(query: types.CallbackQuery):
    await query.message.answer('🔮 Главное меню', reply_markup=await kb.menu())
    
# Клавиатура со списком потоков 
