from pydantic import BaseModel, Field


class CreateReactionRequest(BaseModel):
    objective: str = Field(min_length=1)
    reaction: str = Field(min_length=1)
    reactor: str = Field(min_length=1)
