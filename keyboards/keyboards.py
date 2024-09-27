from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from lexicon.lexicon import LEXICON_RU


def keyboard_ground():
    grant_ground_names = LEXICON_RU['grant_ground_names']
    kb_builder: ReplyKeyboardBuilder = ReplyKeyboardBuilder()
    buttons: list[KeyboardButton] = [
        KeyboardButton(text=grant_ground_names[i]) for i in range(len(grant_ground_names))]
    kb_builder.row(*buttons, width=3)
    return kb_builder.as_markup(resize_keyboard=True)


def keyboard_amount():
    grant_amount_names = LEXICON_RU['grant_amount_names']
    kb_builder: ReplyKeyboardBuilder = ReplyKeyboardBuilder()
    buttons: list[KeyboardButton] = [
        KeyboardButton(text=grant_amount_names[i]) for i in range(len(grant_amount_names))
    ]
    kb_builder.row(*buttons, width=3)
    return kb_builder.as_markup(resize_keyboard=True)


keyboard_bool = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Да')],
    [KeyboardButton(text='Нет')]
])

keyboard_experience = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Выигрывал больше двух раз'), KeyboardButton(text='Подавался, но не выигрывал')],
    [KeyboardButton(text='Выигрывал один раз'), KeyboardButton(text='Нет')],
])

keyboard_role = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Автор'), KeyboardButton(text='Участник'), KeyboardButton(text='Не помню')],
])

BUTTON_CANCEL = KeyboardButton(text="❌ Cancel")


# await message.answer(LEXICON_RU['GrantExperience'],
#                      reply_markup=InlineKeyboardMarkup(inline_keyboard=[
#                          [InlineKeyboardButton(text='Да', callback_data='GrantExperience_yes')],
#                          [InlineKeyboardButton(text='Нет', callback_data='GrantExperience_no')]]))
