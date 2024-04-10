import asyncio
import logging

from aiogram import Bot, Dispatcher
from config import TOKEN
from aiogram.fsm.storage.memory import MemoryStorage

import handlers
import admin

from models import async_main

async def main():
    bot = Bot(token=TOKEN, parse_mode='HTML')
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(handlers.router_u)
    dp.include_router(admin.router_a)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)
    
async def get_bot():
    return Bot(token=TOKEN, parse_mode='HTML')
    
if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(async_main())
        asyncio.run(main())
    except (KeyboardInterrupt):
        print('Bot stopped!')
        