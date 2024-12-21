from pydantic import BaseModel, Field
from typing import List


class PlayerState(BaseModel):
    user_id: str = Field(..., alias='userId')
    latitude: float
    longitude: float


class GameState(BaseModel):
    player: PlayerState
    other_players: List[PlayerState] = Field(..., alias='otherPlayers')
