import datetime
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from bot_instance import bot

from database.crud import get_all_reminds, get_user_by_id, del_remind, get_user, get_additional_remind_status

from logic.email_sender import send_email

STICKER = "CAACAgIAAxkBAAEP2aNpIncyisYoX1m97tFnTWJ6G8qe-wACXk4AAuKwSUqCCQ9LDdUQ5jYE"

scheduler = AsyncIOScheduler()

async def _scheduled(chat_id: int, text: str, remind_id: int, to: str=None, content: str=None):
    user = await get_user(tg_id=chat_id)
    user_chat = await bot.get_chat(chat_id)
    message = f"{user_chat.full_name}, напоминаю тебе:\n\n 🔔 <b><em>{text}</em></b>"

    await bot.send_sticker(chat_id=chat_id, sticker=STICKER)
    await bot.send_message(chat_id=chat_id, text=message)
    if user.email:
        await send_email(to=user.email, content=message) 

    await del_remind(rid=remind_id)


async def schedule_job(run_at: datetime, args):
    status = await get_additional_remind_status(tg_id=args[0])
    if status:
        run_at_additional = run_at + datetime.timedelta(minutes=20)
        scheduler.add_job(func=_scheduled, trigger='date', run_date=run_at_additional, args=args)

    scheduler.add_job(func=_scheduled, trigger='date', run_date=run_at, args=args)

async def schedule_all():
    reminds = await get_all_reminds()
    for remind in reminds:
        user = await get_user_by_id(uid=int(remind.user_id))
        await schedule_job(run_at=remind.date, args=[user.tg_id, remind.text, remind.id])



 

