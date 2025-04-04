import asyncio

from aiogram import Bot, Dispatcher
from config import TOKEN
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.default import DefaultBotProperties

import handlers
import admin

from models import async_main

async def main():
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode='HTML'))
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(handlers.router_u)
    admin.router_a.bot = bot
    dp.include_router(admin.router_a)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    try:
        asyncio.run(async_main())
        asyncio.run(main())
    except (KeyboardInterrupt):
        print('Bot stopped!')