from pydantic import BaseModel, Field
from typing import List, Optional


class SongState(BaseModel):
    id: str
    title: str
    bpm: int
    onset: float


class PlayerState(BaseModel):
    user_id: str = Field(..., alias='userId')
    username: str
    latitude: float
    longitude: float
    is_main: bool = Field(..., alias='isMain')


class GameState(BaseModel):
    players: List[PlayerState]
    song: Optional[SongState] = None
