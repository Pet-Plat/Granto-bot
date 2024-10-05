import asyncio
import logging
import sys

from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.scene import SceneRegistry
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove, CallbackQuery

import keyboards
from lexicon.lexicon import LEXICON_RU

formatter = logging.Formatter(
    fmt='#%(levelname)-8s [%(asctime)s] - %(filename)s:'
        '%(lineno)d - %(name)s:%(funcName)s - %(message)s'
)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
stdout_logger = logging.StreamHandler(sys.stdout)
stdout_logger.setFormatter(formatter)
logger.addHandler(stdout_logger)

router = Router()
registry = SceneRegistry(router)
# router.message.filter(IsInList(message.from_user.id))


user_dict: dict[int, dict[str, str | int | bool]] = {}


class ExperienceInObtainingGrants(StatesGroup):
    fill_initials = State()
    fill_exp = State()
    fill_leader = State()
    fill_ground = State()
    fill_amount = State()
    check_grant_ground = State()
    fill_opportunities = State()


class LegalPossibilities(StatesGroup):
    opportunities = State()





@router.callback_query(F.data == 'start' or StateFilter(ExperienceInObtainingGrants.fill_initials))
async def get_initials(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(text=LEXICON_RU['initials'], reply_markup=ReplyKeyboardRemove())
    await state.set_state(ExperienceInObtainingGrants.fill_exp)
    logger.info('Бот out get_initials')


@router.message(StateFilter(ExperienceInObtainingGrants.fill_exp))
async def get_exp(message: Message, state: FSMContext):
    logger.info('Бот in get_exp')

    if not message.text.isalpha():
        await message.answer(text='Введите Ваше ФИО заново (оно должно состоять только из букв)')
    else:
        await state.update_data(full_name=message.text)

        await message.answer(LEXICON_RU['GrantExperience'],
                             reply_markup=keyboards.keyboard_experience)
        await state.set_state(ExperienceInObtainingGrants.fill_leader)


@router.message(StateFilter(ExperienceInObtainingGrants.fill_leader))
async def get_leader(message: Message, state: FSMContext):
    logger.info(message.text)
    await state.update_data(grant_experience=message.text)

    if message.text == 'Нет':
        logger.info('Логгер видит что ответ нет')  # not finish
        await message.answer(text=LEXICON_RU['skip_first_block'],
                             reply_markup=ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Продолжим!')]]))

        await state.set_state(ExperienceInObtainingGrants.fill_opportunities)
    else:
        await message.answer('Были руководителем (автором проекта) или участником?',
                             reply_markup=keyboards.keyboard_role)
        await state.set_state(ExperienceInObtainingGrants.fill_ground)


@router.message(StateFilter(ExperienceInObtainingGrants.fill_ground))
async def get_ground(message: Message, state: FSMContext):
    logger.info(message.text)
    await state.update_data(project_role=message.text)
    await message.answer(text=LEXICON_RU['ground'],
                         reply_markup=keyboards.keyboard_ground())
    await state.set_state(ExperienceInObtainingGrants.fill_amount)


@router.message(StateFilter(ExperienceInObtainingGrants.check_grant_ground))
async def check_grant_ground(message: Message, state: FSMContext):
    logger.info(message.text)

    await message.answer(text='Впиши название грантового фонда',
                         reply_markup=ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Следующий вопрос')]]))

    await state.set_state(ExperienceInObtainingGrants.fill_amount)


@router.message(StateFilter(ExperienceInObtainingGrants.fill_amount))
async def get_amount(message: Message, state: FSMContext):
    logger.info(message.text)
    if message.text == 'Другое':
        logger.info(message.text)
        await message.answer(text='Впиши название грантового фонда',
                             reply_markup=ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Следующий вопрос')]]))
    else:
        await state.update_data(grant_platform=message.text)
        await message.answer(text=LEXICON_RU['grant_amount'],
                             reply_markup=keyboards.keyboard_amount())
        await state.set_state(ExperienceInObtainingGrants.fill_opportunities)


@router.message(StateFilter(ExperienceInObtainingGrants.fill_opportunities))
async def get_opportunities(message: Message, state: FSMContext):
    await state.update_data(grant_amount=message.text)
    # await state.clear()
    # user_dict[message.from_user.id] = await state.get_data()
    logger.info('qweqe')
    await message.answer(text=LEXICON_RU['opportunities'],
                         reply_markup=keyboards.keyboard_opportunities)

    await state.set_state(LegalPossibilities.opportunities)


@router.message(StateFilter(LegalPossibilities.opportunities))
async def opportunities_answer(message: Message, state: FSMContext):
    opportunities_category = message.text

    await message.answer(
        text='Уточните вашу категорию',
        reply_markup=keyboards.keyboard_opportunities_answer[
            LEXICON_RU['keyboard_opportunities_text'].index(opportunities_category)
        ]
    )





@router.message()
async def catch_trash(message: Message):
    await message.answer(
        text='Выберите один из предложенных вариантов или начните сначала нажав на команду /start !',
        reply_markup=ReplyKeyboardRemove()
    )