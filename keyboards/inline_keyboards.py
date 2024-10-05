from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

from lexicon.lexicon import LEXICON_RU

keyboard_opportunities_answer = [
    InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=LEXICON_RU["keyboard_opportunities_answer"][j][i],
                                     callback_data=LEXICON_RU["keyboard_opportunities_answer"][j][i])
            ] for i in range(len(LEXICON_RU['keyboard_opportunities_answer'][j]))
        ]
    ) for j in range(len(LEXICON_RU['keyboard_opportunities_answer']))
]

print(keyboard_opportunities_answer[4])
