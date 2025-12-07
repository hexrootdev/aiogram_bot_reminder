from datetime import  datetime, timedelta

from aiogram.filters import Command, CommandStart
from aiogram.types import Message, CallbackQuery, FSInputFile

from aiogram import Router, F

from keyboards.reply import get_help_kb, get_date_remind_kb, get_settings_kb
from keyboards.inline import get_reminds_kb, get_confirmation_kb
from fsm.fsm import FSMContext, SetRemindFSM, SetEmailFSM, DelEmailFSM

from logic.reminder import schedule_job
from logic.email_sender import get_validated_email

from database.crud import add_user, get_user, clear_all_tables, add_remind, del_remind, is_count_reminds_less_fifteen, set_or_del_email, switch_additional_remind_status, get_additional_remind_status


STICKER1 = "CAACAgIAAxkBAAM1aRcrAAGM1owqpHPMU1mYjxCIWvymAALNPwAClgfhSanErHL2RQ_1NgQ"
STICKER2 = "CAACAgIAAxkBAAEP4jZpKELK-MuMopnaHyTj0FsZT2c6LAACREMAAm8U2EmRUPF4DGjb_jYE"

router = Router()

@router.message(CommandStart())
async def start_cmd(message: Message):
    await add_user(tg_id=int(message.from_user.id))

    await message.answer("<b>Даров, че как? 🤠\n\nЗдесь ты можешь поставить <em>любое напоминание</em>, \n" \
    "чтобы ты не забыл выполнить <em>очередное дельце</em>, \nкоторое откладывал на понедельник... 🤥\n\n" \
    "Используй команду <em>/help</em> или <em>клавиатуру ниже</em> 👇</b>",
    reply_markup=get_help_kb())
    
    
@router.message(Command("help"))
async def help_cmd(message: Message):
    await message.answer_sticker(sticker=STICKER1,
                                 reply_markup=get_help_kb())
    uid = int(message.from_user.id)
    status = await get_additional_remind_status(tg_id=uid)
    print(status)
    
@router.message(Command("dt"))
async def del_table_users(message: Message):
    try:
        await clear_all_tables()
        await message.answer("Таблицы Users и Reminds очищены.")
    except Exception as e:
        await message.answer("Что-то пошло не так...")
        print(e)    
    
    

@router.message(F.text == "Мои напоминания 📝")    
async def my_remind_cmd(message: Message):
    await message.answer("<b>Ваши напоминания (нажатие - удаление)</b>",
                          reply_markup=await get_reminds_kb(tg_id=int(message.from_user.id)))
    
@router.callback_query(F.data.startswith("remind_"))
async def del_remind_cmd(callback: CallbackQuery):
    _, rid = str(callback.from_user.id).split()
    await del_remind(rid=int(rid))  
    await callback.answer("Напоминание удалено.") 


@router.message(F.text == "Новое напоминание ➕")    
async def new_remind_cmd(message: Message, state: FSMContext):
    uid = int(message.from_user.id)
    count = await is_count_reminds_less_fifteen(uid)

    if count:
        await message.answer("Выберите <b>ниже</b> 👇", reply_markup=get_date_remind_kb())
        await state.set_state(SetRemindFSM.date)
    else:
        await message.answer("⚠️ Достигнут лимит напоминаний! <b><em>(20)</em></b>")


@router.message(F.text == "Завтра", SetRemindFSM.date)
async def set_tomorrow_cmd(message: Message, state: FSMContext):
    remind_day = datetime.now() + timedelta(days=1)
    
    await message.edit_text("Введите текст напоминания в формате (без кавычек) <b><em>`текст`</em></b>")

    await state.update_data(remind_date=remind_day)
    await state.set_state(SetRemindFSM.message)
  
@router.message(F.text == "Послезавтра", SetRemindFSM.date)
async def set_aftertomorrow_cmd(message: Message, state: FSMContext):
    remind_day = datetime.now() + timedelta(days=2)
    
    await message.edit_text("Введите текст напоминания в формате (без кавычек) <b><em>`текст`</em></b>")
    
    await state.update_data(remind_date=remind_day)
    await state.set_state(SetRemindFSM.message)

@router.message(F.text == "На след. неделе", SetRemindFSM.date)
async def set_next_week_cmd(message: Message, state: FSMContext):
    remind_day = datetime.now() + timedelta(days=7)

    await message.edit_text("Введите текст напоминания в формате (без кавычек) <b><em>`текст`</em></b>")
    
    await state.update_data(remind_date=remind_day)
    await state.set_state(SetRemindFSM.message)

@router.message(SetRemindFSM.message)
async def set_message_cmd(message: Message, state: FSMContext):
    await message.answer(f"Сообщение: `{message.text}`")

    user_id = int(message.from_user.id)
    remind_day = (await state.get_data()).get("remind_date")

    remind = await add_remind(tg_id=user_id, date=remind_day, text=message.text)

    await schedule_job(run_at=remind_day, args=[user_id, message.text, remind.id])

    await state.clear()
    

@router.message(F.text == "Другое", SetRemindFSM.date)
async def get_another_date_cmd(message: Message, state: FSMContext):
    await message.answer("Введите дату, время и текст напоминания СТРОГО в формате (без кавычек) 👇\n\n"
                         "<b><em>`день.месяц.год час:минута - текст`</em></b>")   
    
    await state.set_state(SetRemindFSM.data)

@router.message(SetRemindFSM.data)
async def set_date_and_text_cmd(message: Message, state: FSMContext): 
    str_date, text = message.text.split(" - ")
    user_id = int(message.from_user.id)

    try:
        date = datetime.strptime(str_date, "%d.%m.%Y %H:%M")
        remind = await add_remind(tg_id=user_id, date=date, text=text)

        await schedule_job(run_at=date, args=[user_id, text, remind.id])

        await state.clear()
    except ValueError:
        await message.answer("<b>Введите в ПРАВИЛЬНОМ формате !!!</b>")    
    
    await message.answer(f"Время и сообщение: {message.text}")

    

@router.message(F.text == "Настройки ⚙️")    
async def settings_cmd(message: Message):
    await message.answer_sticker(sticker=STICKER2, reply_markup=get_settings_kb())

@router.message(F.text == "Указать/убрать Email 📩")
async def set_or_email_cmd(message: Message, state: FSMContext):
    uid = int(message.from_user.id)
    user = await get_user(tg_id=uid)

    if user.email:
        await message.answer("Убрать Ваш Email для отправки напоминаний?",
                              reply_markup=get_confirmation_kb())
        await state.set_state(DelEmailFSM.confirmation)
    else:
        await message.answer("<b>Напишите Ваш <em>Email</em></b> 👇")    
        await state.set_state(SetEmailFSM.email)

@router.callback_query(F.data.startswith("confirm_"), DelEmailFSM.confirmation)
async def remove_email_cmd(callback: CallbackQuery, state: FSMContext):
    uid = int(callback.from_user.id)
    _, value = str(callback.data).split("_")

    if value == "yes":
        await set_or_del_email(tg_id=uid, email=None)
        await callback.answer("Вы убрали email.")
    elif value == "no":
        await callback.answer("Вы отменили действие.")    
    await state.clear()   

@router.message(SetEmailFSM.email) 
async def set_email_cmd(message: Message, state: FSMContext):
    uid = int(message.from_user.id)
    email = message.text
    valid_email = get_validated_email(email=email)
    
    if valid_email:
        await set_or_del_email(tg_id=uid, email=valid_email) 
        await message.answer(f"Теперь вам будут приходить напоминания на почту <em>{valid_email}</em>\n")
    else:
        await message.answer("Кажется, вы ввели не совсем адрес эл. почты...\nПовторите попытку правильно.")    
    await state.clear()

@router.message(F.text == "Включить/отключить доп. напоминание 🎯")
async def switch_additional_remind_cmd(message: Message):
    uid = int(message.from_user.id)
    status = await switch_additional_remind_status(tg_id=uid)
    if status:
        await message.answer("✅ Вы <b>включили</b> доп. напоминание <em>(через 20 минут после основного)</em>")
    else:
        await message.answer("📴 Вы <b>отключили</b> доп. напоминание.")    
