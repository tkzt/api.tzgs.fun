from enum import Enum
from pydantic import BaseModel, Field


class ReactionObjective(str, Enum):
    TKZT_CN = "tkzt.cn"
    FINE_WEATHER_TKZT_CN = "fine-weather.tkzt.cn"


class CreateReactionRequest(BaseModel):
    objective: ReactionObjective = Field(min_length=1)
    reaction: str = Field(min_length=1, max_length=2)
    reactor: str = Field(min_length=1, max_length=256)
