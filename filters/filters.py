from aiogram.types import Message
from aiogram.filters import BaseFilter
from config_data.user_config import UserActionsInfo, users


class AnswerType(BaseFilter):
    def __init__(self, command: str):
        self.command = command


    async def __call__(self, message: Message) -> bool:
        return users[message.from_user.id].next_action == self.command


class IsInList(BaseFilter):
    def __init__(self, id):
        self.id = id


    async def __call__(self, message: Message) -> bool:
        if not self.id in users:
            users[self.id] = UserActionsInfo(self.id)
