import asyncio
import logging
import sys

from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.scene import Scene, on, After, SceneRegistry
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove, CallbackQuery

import keyboards
from lexicon.lexicon import LEXICON_RU

formatter = logging.Formatter(
    fmt='#%(levelname)-8s [%(asctime)s] - %(filename)s:'
        '%(lineno)d - %(name)s:%(funcName)s - %(message)s'
)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
stdout_logger = logging.StreamHandler(sys.stdout)
stdout_logger.setFormatter(formatter)
logger.addHandler(stdout_logger)

router = Router()
registry = SceneRegistry(router)
# router.message.filter(IsInList(message.from_user.id))


user_dict: dict[int, dict[str, str | int | bool]] = {}


class FSMFillForm(StatesGroup):
    fill_initials = State()
    fill_exp = State()
    fill_leader = State()
    fill_ground = State()
    fill_amount = State()
    check_grant_ground = State()
    fill_opportunities = State()


@router.callback_query(F.data == 'start' or StateFilter(FSMFillForm.fill_initials))
async def get_initials(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(text=LEXICON_RU['initials'], reply_markup=ReplyKeyboardRemove())
    await state.set_state(FSMFillForm.fill_exp)
    logger.info('Бот out get_initials')


@router.message(StateFilter(FSMFillForm.fill_exp))
async def get_exp(message: Message, state: FSMContext):
    logger.info('Бот in get_exp')

    if not message.text.isalpha():
        await message.answer(text='Введите Ваше ФИО заново (оно должно состоять только из букв)')
    else:
        await state.update_data(name=message.text)

        await message.answer(LEXICON_RU['GrantExperience'],
                             reply_markup=keyboards.keyboard_experience)
        await state.set_state(FSMFillForm.fill_leader)


@router.message(StateFilter(FSMFillForm.fill_leader))
async def get_leader(message: Message, state: FSMContext):
    logger.info(message.text)
    await state.update_data(name=message.text)

    if message.text == 'Нет':
        logger.info('Логгер видит что ответ нет')  # not finish
        await message.answer(text=LEXICON_RU['skip_first_block'],
                             reply_markup=ReplyKeyboardRemove())
        await asyncio.sleep(0.2)
        await message.answer(text=LEXICON_RU['get_opportunities'])

        await state.set_state(FSMFillForm.fill_opportunities)
    else:
        await message.answer('Были руководителем (автором проекта) или участником?',
                             reply_markup=keyboards.keyboard_role)
        await state.set_state(FSMFillForm.fill_ground)


@router.message(StateFilter(FSMFillForm.fill_ground))
async def get_ground(message: Message, state: FSMContext):
    logger.info(message.text)
    await state.update_data(name=message.text)
    await message.answer(text=LEXICON_RU['ground'],
                         reply_markup=keyboards.keyboard_ground())
    await state.set_state(FSMFillForm.fill_amount)


@router.message(StateFilter(FSMFillForm.check_grant_ground))
async def check_grant_ground(message: Message, state: FSMContext):
    logger.info(message.text)

    await message.answer(text='Впиши название грантового фонда',
                         reply_markup=ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Следующий вопрос')]]))

    await state.set_state(FSMFillForm.fill_amount)


@router.message(StateFilter(FSMFillForm.fill_amount))
async def get_amount(message: Message, state: FSMContext):
    logger.info(message.text)
    if message.text == 'Другое':
        logger.info(message.text)
        await message.answer(text='Впиши название грантового фонда',
                             reply_markup=ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Следующий вопрос')]]))
    else:
        await state.update_data(name=message.text)
        await message.answer(text=LEXICON_RU['grant_amount'],
                             reply_markup=keyboards.keyboard_amount())
        await state.set_state(FSMFillForm.fill_opportunities)


@router.message(StateFilter(FSMFillForm.fill_opportunities))
async def get_opportunities(message: Message, state: FSMContext):
    await state.update_data(name=message.text)

    await message.answer('Конец первого блока')
    user_dict[message.from_user.id] = await state.get_data()
    await state.clear()

    if message.from_user.id in user_dict:
        # await state.set_state(FSMFillForm.fill_opportunities)
        await message.answer('Ответы записаны')
    else:
        await message.answer('Вы не ответили на вопросы')


# class CancellableScene(Scene):
#     """
#     This scene is used to handle cancel and back buttons,
#     can be used as a base class for other scenes that needs to support cancel and back buttons.
#     """
#     @on.message(F.text.casefold() == keyboards.BUTTON_CANCEL.text.casefold(), after=After.exit())
#     async def handle_cancel(self, message: Message):
#         await message.answer("Для того, чтобы начать сначала введите команду /start",
#                              reply_markup=ReplyKeyboardRemove())
#
#
# class ExperienceInObtainingGrants(CancellableScene, state='ExperienceInObtainingGrants'):
#     pass
#
#
# # All scenes at register time converts to Routers and includes into specified router.
# registry.add(
#     ExperienceInObtainingGrants,
#
# )