import asyncio
import logging

from aiogram import Bot, Dispatcher
from config import TOKEN
from aiogram.fsm.storage.memory import MemoryStorage

import handlers
import admin


async def main():
    bot = Bot(token=TOKEN, parse_mode='HTML')
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(handlers.router_u)
    dp.include_router(admin.router_a)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)
    
    
if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except (KeyboardInterrupt):
        print('Bot stopped!')