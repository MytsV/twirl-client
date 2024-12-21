from pydantic import BaseModel, Field
from typing import List


class PlayerState(BaseModel):
    user_id: str = Field(..., alias='userId')
    latitude: float
    longitude: float
    is_main: bool = Field(..., alias='isMain')


class GameState(BaseModel):
    players: List[PlayerState]
