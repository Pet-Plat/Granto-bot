from aiogram import Router
from aiogram.types import Message
from lexicon.lexicon import LEXICON_RU
from aiogram.filters import Command


router = Router()

@router.message()
async def send_sth(message: Message):
    try:
        await message.send_copy(chat_id=message.chat.id)
    except TypeError:
        await message.reply(text=LEXICON_RU['pass'])
