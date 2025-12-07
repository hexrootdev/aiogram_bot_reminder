from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from database.crud import get_reminds_user

async def get_reminds_kb(tg_id: int) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    
    reminds = await get_reminds_user(tg_id=tg_id)
    for remind in reminds:
        kb.row(InlineKeyboardButton(text=f"{remind.date} - {remind.text}", callback_data=f"remind_{remind.id}"))
    return kb.as_markup()    


def get_confirmation_kb():
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✅", callback_data="confirm_yes"),
         InlineKeyboardButton(text="❌", callback_data="confirm_no")]
    ])

    return kb

