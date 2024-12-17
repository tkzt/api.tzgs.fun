from uuid import UUID
from fastapi import APIRouter
from fastapi_async_sqlalchemy import db
from sqlmodel import select

from models.db.reaction import Reaction
from models.reaction import CreateReactionRequest
from utils.response import BaseResponse, make_response
from utils.logger import logger


router = APIRouter(prefix="/reactions")


@router.get("", response_model=BaseResponse[list[Reaction]])
async def get_reactions():
    reactions = (await db.session.scalars(select(Reaction))).all()
    return make_response(data=reactions)


@router.post("", response_model=BaseResponse[Reaction])
async def create_reaction(reaction_request: CreateReactionRequest):
    exists_reaction = await db.session.scalar(
        select(Reaction).where(
            Reaction.reaction == reaction_request.reaction,
            Reaction.reactor == reaction_request.reactor,
        )
    )
    if exists_reaction:
        logger.warning(
            f"Reaction {reaction_request.reaction} by "
            f"{reaction_request.reactor} already exists."
        )
        return make_response(data=exists_reaction)
    reaction = Reaction.model_validate(reaction_request)
    db.session.add(reaction)
    await db.session.commit()
    await db.session.refresh(reaction)
    return make_response(data=reaction)


@router.delete("/{reaction_id}", status_code=204)
async def delete_reaction(reaction_id: UUID):
    reaction = await db.session.get(Reaction, reaction_id)
    if not reaction:
        logger.warning(f"Reaction {reaction_id} not found")
        return
    await db.session.delete(reaction)
    await db.session.commit()
