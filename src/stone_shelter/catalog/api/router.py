"""Register a stone and its accompanying case through the HTTP API."""

from typing import Annotated

from fastapi import APIRouter, Depends, status

from stone_shelter.api.ingestion_contracts import (
    StoneRegistrationRequest,
    StoneRegistrationResponse,
)
from stone_shelter.application.register_stone import RegisterStoneService
from stone_shelter.bootstrap.dependencies import get_register_stone_service

router = APIRouter(prefix="/api/v1/stones", tags=["stones"])


@router.post(
    "",
    response_model=StoneRegistrationResponse,
    status_code=status.HTTP_201_CREATED,
)
async def register_stone(
    request: StoneRegistrationRequest,
    service: Annotated[RegisterStoneService, Depends(get_register_stone_service)],
) -> StoneRegistrationResponse:
    created_id = await service.register(request)
    return StoneRegistrationResponse(id=created_id)
