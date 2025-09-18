from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
import json
from pathlib import Path

router = Router()

m = None

def load_m():
    global m
    path = Path("Messages/messages.json")
    with open(path, "r", encoding="utf-8") as f:
        m = json.load(f)


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
						m["start"]["message"],
            reply_markup=reg_butt)
