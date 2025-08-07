from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

router = Router()

@router.message(CommandStart(deep_link=True))
async def start_cmd(message: Message, command: CommandStart):
    args = command.args
    if args == "reg":
        reg_butt = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="Записаться", callback_data="register")]
            ])
        await message.answer(
            "Привет\n\n"
            "Нажмите кнопку ниже, чтобы начать.",
            reply_markup=reg_butt)
