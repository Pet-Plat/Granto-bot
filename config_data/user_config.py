from dataclasses import dataclass
from aiogram.types import Message


@dataclass
class User():
    def __init__(self, user_id: int):
        self.user_id = user_id
    is_admin = None


@dataclass
class UserActionsInfo(User):
    # first block
    def __init__(self, user_id: int):
        super().__init__(user_id)
        
    _grant_experience: int | bool | str = None
    _project_role: str = None
    _grant_platform: str | None = None
    _grant_amount: int | None = None
    
    # second block
    _grant_opportunities: str = None


    next_action: str | None = 'grant_experience'


users: dict[int:UserActionsInfo] = {818626498: UserActionsInfo(818626498)}