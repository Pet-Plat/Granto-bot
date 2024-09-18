from dataclasses import dataclass
from aiogram import Bot, Dispatcher
from environs import Env
from typing import List

@dataclass
class DatabaseConfig:
    database: str
    db_host: str          # URL-адрес базы данных
    db_user: str          # Username пользователя базы данных
    db_password: str 


@dataclass
class TgBot:
    token: str
    admin_ids: List[int]


@dataclass
class Config:
    tg_bot: Bot
    db: DatabaseConfig
    

def load_config(path: str | None = None) -> Config:
    env: Env = Env()
    env.read_env(path)

    return Config(
        tg_bot=TgBot(
            token=env('BOT_TOKEN'),
            admin_ids=list(map(int, env.list('ADMIN_IDS')))
        ),
        db=DatabaseConfig(
            database=env('DATABASE'),
            db_host=env('DB_HOST'),
            db_user=env('DB_USER'),
            db_password=env('DB_PASSWORD')
        )
    )