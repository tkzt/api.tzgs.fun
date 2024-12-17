from sqlmodel import Field

from models.db import BaseDBModel


class BaseReaction(BaseDBModel):
    reaction: str = Field(min_length=1, nullable=False)
    reactor: str = Field(min_length=1, nullable=False)


class Reaction(BaseReaction, table=True):
    pass
