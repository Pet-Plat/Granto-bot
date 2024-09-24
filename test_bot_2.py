from __future__ import annotations

import sys
import logging
import asyncio

from typing import TypedDict

from aiogram.client.default import DefaultBotProperties

from config_data.config import load_config, Config
# from handlers import user_handlers

from aiogram import Bot, Dispatcher, F, html
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state, State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
# from aiogram.fsm.scene import After, Scene, SceneRegistry, on
from aiogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    Message,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
)

from lexicon.lexicon import LEXICON_RU

formatter = logging.Formatter(
    fmt='#%(levelname)-8s [%(asctime)s] - %(filename)s:'
        '%(lineno)d - %(name)s:%(funcName)s - %(message)s'
)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
stdout_logger = logging.StreamHandler(sys.stdout)
# stdout_logger.addFilter()
stdout_logger.setFormatter(formatter)
logger.addHandler(stdout_logger)

user_dict: dict[int, dict[str, str | int | bool]] = {}

config: Config = load_config()

bot = Bot(token=config.tg_bot.token, default=DefaultBotProperties(parse_mode='HTML'))
dp = Dispatcher()
# dp.include_router(user_handlers.router)

logger.info('Бот был успешно запущен')


class FSMFillForm(StatesGroup):
    fill_initials = State()
    fill_exp = State()
    fill_leader = State()
    fill_opportunities = State()


@dp.message(CommandStart())
async def get_initials(message: Message, state: FSMContext):
    await message.answer(text='Введите ваше ФИО')
    await state.set_state(FSMFillForm.fill_exp)
    logger.info('Бот out get_initials')


@dp.message(StateFilter(FSMFillForm.fill_exp))
async def get_exp(message: Message, state: FSMContext):
    logger.info('Бот in get_exp')
    await state.update_data(name=message.text)

    await message.answer('Do you have any exp?')
    await state.set_state(FSMFillForm.fill_leader)


@dp.message(StateFilter(FSMFillForm.fill_leader))
async def get_leader(message: Message, state: FSMContext):
    logger.info(message.text)
    await state.update_data(name=message.text)

    if message.text == 'Нет':
        logger.info('Логгер видит что ответ нет')
        await message.answer('Какие есть возможности на настоящий момент для подачи '
                             'проекта на грант(юридическая основа для подачи на грант?')

        await state.set_state(FSMFillForm.fill_opportunities)
    else:
        await message.answer('Были руководителем(автором проекта) или участником?')
        await state.set_state(FSMFillForm.fill_opportunities)


@dp.message(StateFilter(FSMFillForm.fill_opportunities))
async def get_opportunities(message: Message, state: FSMContext):
    await state.update_data(name=message.text)

    await message.answer('Выберите категорию:')
    user_dict[message.from_user.id] = await state.get_data()
    await state.clear()

    if message.from_user.id in user_dict:
        # await state.set_state(FSMFillForm.fill_opportunities)
        await message.answer('End')
    else:
        await message.answer('Вы не ответили на вопросы')


# async def main():
#     config: Config = load_config()

#     bot = Bot(token=config.tg_bot.token, parse_mode='HTML')
#     dp = Dispatcher()
#     dp.include_router(user_handlers.router)

#     logger.info('Бот был успешно запущен')

# await bot.delete_webhook(drop_pending_updates=True)
dp.run_polling(bot)

# asyncio.run(main())
