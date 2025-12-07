from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

def get_help_kb():
    kb = ReplyKeyboardMarkup(
         keyboard=[
         [
            KeyboardButton(text="Мои напоминания 📝"),
            KeyboardButton(text="Новое напоминание ➕")
         ],
         [
            KeyboardButton(text="Настройки ⚙️")
         ]
        ],
        resize_keyboard=True
    )
    return kb

def get_date_remind_kb():
    kb = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text="Завтра"), KeyboardButton(text="Послезавтра"), KeyboardButton(text="На след. неделе")],
        [KeyboardButton(text="Другое")]
    ], resize_keyboard=True)  

    return kb

def get_settings_kb():
    kb = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text="Указать/убрать Email 📩")],
        [KeyboardButton(text="Включить/отключить доп. напоминание 🎯")]
    ], resize_keyboard=True)
    return kb