from __future__ import annotations

import sys
import logging
import asyncio

from environs import Env
from typing import TypedDict
from config_data.config import load_config, Config

from aiogram import Bot, Dispatcher, F, html
from aiogram.filters import Command, CommandStart
from aiogram.fsm.scene import After, Scene, SceneRegistry, on
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


BUTTON_CANCEL = KeyboardButton(text="❌ Cancel")


class CancellableScene(Scene):
    """
    This scene is used to handle cancel and back buttons,
    can be used as a base class for other scenes that needs to support cancel and back buttons.
    """

    @on.message(F.text.casefold() == BUTTON_CANCEL.text.casefold(), after=After.exit())
    async def handle_cancel(self, message: Message):
        await message.answer("Для того, чтобы начать сначала введите команду /start", reply_markup=ReplyKeyboardRemove())


class GrantExperience(CancellableScene, state='GrantExperience'):
    @on.message.enter()  # Marker for handler that should be called when a user enters the scene.
    async def on_enter(self, message: Message):
        await message.answer(
            LEXICON_RU['GrantExperience'],
            reply_markup=ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Да'), KeyboardButton(text='Нет'), BUTTON_CANCEL]], resize_keyboard=True),
        )

    @on.callback_query.enter()  # different types of updates that start the scene also supported.
    async def on_enter_callback(self, callback_query: CallbackQuery):
        await callback_query.answer()
        await self.on_enter(callback_query.message)


class UserInitials(CancellableScene, state='initials'):
    # @on.message.enter()
    @on.message
    async def get_initials(message: Message):
        logger.debug("i'm in get_initials")
        await message.answer(
            text=LEXICON_RU['initials'],
            reply_markup=ReplyKeyboardRemove()
        )
        initials = message.text
        logger.debug(initials)


class PersonalLicense(
    Scene, 
    reset_data_on_enter=True,
    callback_query_without_state=True,
):
    # @on.callback_query(F.data == "agree", after=After.goto(GrantExperience))
    # async def demo_callback(self, callback_query: CallbackQuery):
    #     await callback_query.answer(cache_time=0, reply_markup=ReplyKeyboardRemove())
    #     await callback_query.message.delete_reply_markup()

    @on.callback_query(F.data == "agree", after=After.goto(UserInitials))
    async def demo_callback(self, callback_query: CallbackQuery):
        logger.debug("i'm in demo_callback")
        await callback_query.message.answer(text=LEXICON_RU['initials'])
        await callback_query.answer(cache_time=0, reply_markup=ReplyKeyboardRemove())
        await callback_query.message.delete_reply_markup()

    @on.message(CommandStart())
    async def start(self, message: Message):
        await message.answer(
            text=LEXICON_RU["/start"],
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(text=LEXICON_RU["agree"], url='https://ya.ru')],
                    [InlineKeyboardButton(text='Даю согласие', callback_data="agree")]
                    ]
            ),
        )


def create_dispatcher() -> Dispatcher:
    dispatcher = Dispatcher()

    # Scene registry should be the only one instance in your application for proper work.
    # It stores all available scenes.
    # You can use any router for scenes, not only `Dispatcher`.
    registry = SceneRegistry(dispatcher)
    # All scenes at register time converts to Routers and includes into specified router.
    registry.add(
        GrantExperience,
        PersonalLicense,
        UserInitials,
    )

    return dispatcher


async def main():

    config: Config = load_config()
    
    bot = Bot(token=config.tg_bot.token)
    dp = create_dispatcher()

    logger.info('Бот был успешно запущен')

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)
    

asyncio.run(main())


# def main() -> None:
#     dp = create_dispatcher()
#     config: Config = load_config()
#     bot = Bot(token=config.tg_bot.token)

#     logger.info('Бот был успешно запущен')

#     dp.run_polling(bot)


# if __name__ == "__main__":
#     # Recommended to use CLI instead of this snippet.
#     # `aiogram run polling scene_example:create_dispatcher --token BOT_TOKEN --log-level info`
#     main()