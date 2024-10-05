from sqlalchemy import create_engine, MetaData, Table, String, Integer, Boolean, Column, Text, DateTime, ForeignKey
from datetime import datetime

from config_data.config import Config, load_config
from handlers.other_handlers import FSMFillForm

config: Config = load_config()
engine = create_engine('sqlite:///BOT.db')
engine.connect()
metadata = MetaData()

users = Table(
    'users',
    metadata,
    Column('Id', Integer(), unique=True, primary_key=True),
    Column('User_id', Integer(), unique=True, nullable=False),
    Column('Ref', String(100), nullable=False),
    Column('Is_delete', Boolean(), default=False),
    Column('Is_pay_null', Boolean(), default=False),
    Column('Is_tariff', Boolean(), default=False),
    Column('Create_user', DateTime(), default=datetime.now()),
)

metadata.create_all(engine)
