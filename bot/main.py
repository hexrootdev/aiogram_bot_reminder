import asyncio
from aiogram import Dispatcher

from bot_instance import bot
from handlers.user import router

from database.database import init_db
from logic.reminder import scheduler, schedule_all

dp = Dispatcher()

async def main():
    dp.include_router(router=router)
    
    await init_db()
    scheduler.start()
    await schedule_all()
    await dp.start_polling(bot)
    

if __name__ == "__main__":
    print("Бот запущен.")
    asyncio.run(main()) 
