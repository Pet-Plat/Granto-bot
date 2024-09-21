import logging
import sys

from aiogram import Router
from aiogram.types import Message, KeyboardButton
from lexicon.lexicon import LEXICON_RU
from aiogram.filters import Command
from filters.filters import AnswerType, IsInList
from config_data.user_config import UserActionsInfo, users
from aiogram.utils.keyboard import ReplyKeyboardBuilder


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
# router.message.filter(IsInList(message.from_user.id))

kb_builder = ReplyKeyboardBuilder()


@router.message(AnswerType('grant_experience'))
async def grant_experience(message: Message):
    user = UserActionsInfo(message.from_user.id)
    
    logger.info(users)

    buttons: list[KeyboardButton] = [
        KeyboardButton(text='Да'), KeyboardButton(text='Нет')
    ]
    kb_builder.row(*buttons, width=2)
    await message.answer(
        text=LEXICON_RU['grant_experience'],
        reply_markup=kb_builder.as_markup(resize_keyboard=True, one_time_keyboard=True)
    )
    logger.info('keyboard activated')

    if message.text in ['Да', 'да']:
        user.grant_experience = 'Да'
        user.next_action = 'project_role'
        logger.debug('yes ansver')

    else:
        user.grant_experience = 'Нет'
        next_action = 'grant_opportunities'
    logger.debug(f'user.grant_experience - {user.grant_experience}')
    users[user.user_id] = user



