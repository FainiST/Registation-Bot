from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

router = Router()

class Registr(StatesGroup):
    name = State()
    phone = State()
    usrname = State()

@router.callback_query(F.data == "register")
async def start_registration(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("Введите ваше имя:")
    await state.set_state(Registr.name)

@router.message(Registr.name)
async def process_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Введите ваш номер телефона:")
    await state.set_state(Registr.phone)

@router.message(Registr.phone)
async def process_phone(message: Message, state: FSMContext):
    await state.update_data(phone=message.text)
    username = message.from_user.username or "—"
    await state.update_data(username=username)

    data = await state.get_data()

    await message.answer(
        f"Вы успешно зарегистрировались!\n\n"
        f"Имя: {data['name']}\n"
        f"Телефон: {data['phone']}\n"
        f"TG никнейм: @{data['username']}"
    )

    print("Новая регистрация:", data)  # TODO: сделать сохранение в базу данных

    await state.clear()