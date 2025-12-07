from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

class SetRemindFSM(StatesGroup):
    date = State()
    message = State()
    data = State()
    remind = State()

class SetEmailFSM(StatesGroup):
    email = State()    

class DelEmailFSM(StatesGroup):
    confirmation = State()   