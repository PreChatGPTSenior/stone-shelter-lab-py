"""Catalog HTTP routes. Later bind parameters, invoke catalog use cases or queries, and serialize responses. Keep database queries and business rules out of handlers."""

from typing import Annotated

from fastapi import APIRouter, Depends, status

from stone_shelter.bootstrap.dependencies import get_create_stone_service
from stone_shelter.catalog.application.create_stone import CreateStoneService
from stone_shelter.catalog.contracts import StoneCreateRequest, StoneCreateResponse

router = APIRouter(
    prefix="/api/v1/stones",
    tags=["stones"],
)


@router.post(
    "",
    response_model=StoneCreateResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_stone(
    request: StoneCreateRequest,
    service: Annotated[
        CreateStoneService,
        Depends(get_create_stone_service),
    ],
) -> StoneCreateResponse:
    stone = await service.create(request)
    return StoneCreateResponse.model_validate(stone)
