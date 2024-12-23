from pydantic import BaseModel, Field
from typing import List, Optional

from graphics.common import DEFAULT_BLOB_COLOR


class SongState(BaseModel):
    id: str
    title: str
    bpm: int
    onset: float
    start_timestamp: int = Field(..., alias="startTimestamp")


class PlayerState(BaseModel):
    user_id: str = Field(..., alias="userId")
    username: str
    latitude: float
    longitude: float
    is_main: bool = Field(..., alias="isMain")
    status: str
    last_mark: Optional[str] = Field(default=None, alias="lastMark")
    color: Optional[str] = DEFAULT_BLOB_COLOR


class GameState(BaseModel):
    players: List[PlayerState]
    song: Optional[SongState] = None
    location_title: str = Field(..., alias="locationTitle")
    arrow_combination: Optional[List[str]] = Field(
        default=None, alias="arrowCombination"
    )
