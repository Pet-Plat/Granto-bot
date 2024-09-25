import asyncio
import sys
import logging

from aiogram import Bot, Dispatcher
from config_data.config import Config, load_config
from handlers import other_handlers, user_handlers


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


# Функция конфигурирования и запуска бота
async def main():

    config: Config = load_config()
    
    bot = Bot(token=config.tg_bot.token)
    dp = Dispatcher()
    dp.include_router(user_handlers.router)
    dp.include_router(other_handlers.router)

    logger.info('Бот был успешно запущен')

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)
    

asyncio.run(main())