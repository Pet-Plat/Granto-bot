import logging
import sys 

from aiogram import Router
from aiogram.types import Message, ChatMemberUpdated, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardRemove
from lexicon.lexicon import LEXICON_RU
from aiogram.filters import Command, CommandStart, ChatMemberUpdatedFilter, KICKED


formatter = logging.Formatter(
    fmt='#%(levelname)-8s [%(asctime)s] - %(filename)s:'
        '%(lineno)d - %(name)s:%(funcName)s - %(message)s'
)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
stdout_logger = logging.StreamHandler(sys.stdout)
# stdout_logger.addFilter()
stdout_logger.setFormatter(formatter)
logger.addHandler(stdout_logger)

router = Router()


@router.my_chat_member(ChatMemberUpdatedFilter(member_status_changed=KICKED))
async def process_user_blocked_bot(event: ChatMemberUpdated):
    logger.info(f'Пользователь {event.from_user.id} заблокировал бота')


@router.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer(text=LEXICON_RU['/start'],
                         reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                             [InlineKeyboardButton(text='Согласен', callback_data='start')],
                             [InlineKeyboardButton(text='Ссылка', url='https://ya.ru')]]))
    logger.info('I am out process_start_command')


@router.message(Command(commands='help'))
async def process_help_command(message: Message):
    await message.answer(text=LEXICON_RU['/help'])


@router.message(Command(commands='reset'))
async def process_help_command(message: Message):
    await message.answer(text=LEXICON_RU['/reset'])
    # нужно удалить всю инфу из бд




