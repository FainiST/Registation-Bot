from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

router = Router()

@router.message(CommandStart(deep_link=True))
async def start_cmd(message: Message):
    parts = (message.text or "").split(maxsplit=1)
    arg = parts[1] if len(parts) > 1 else ""
    if arg == "reg":
        reg_butt = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="Записаться", callback_data="register")]
            ])
        await message.answer(
            "Привет друг! \n\n"
            "Мы рады, что ты на Связи! Давай запишемся на мастер-класс",
            reply_markup=reg_butt)
