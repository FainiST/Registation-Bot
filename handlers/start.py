from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

start_cmd = Router()

@start_cmd.message(CommandStart(deep_link=True))
async def start_cmd(message: Message, command: CommandStart):
    args = command.args
    if args == "reg":
        reg_butt = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="Записатся", callback_data="register")]
            ])
        await message.answer(
            "Привет\n\n"
            "Нажмите кнопку ниже, чтобы начать.",
            reply_markup=reg_butt)
    else:
        await message.answer("Начните регистрацию нажав на кнопку в канале")
