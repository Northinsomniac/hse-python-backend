from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, HTTPException, Query, Response
from pydantic import NonNegativeInt, PositiveInt, PositiveFloat, NonNegativeFloat

from typing_extensions import List
from lecture_2.hw.shop_api.storage import item_query as storage

from .contracts import ItemRequest, ItemResponse, ItemPatchRequest

router = APIRouter(prefix="/item")


@router.post("/", status_code=HTTPStatus.CREATED, response_model=ItemResponse)
async def post_item(info: ItemRequest, response: Response) -> ItemResponse:
    entity = storage.add_item(info.as_item_info())

    response.headers["location"] = f"/item/{entity.id}"

    return ItemResponse.from_entity(entity)


@router.get("/{id}", response_model=ItemResponse)
async def get_item_by_id(id: int) -> ItemResponse:
    entity = storage.get_item_by_id(id)
    if not entity:
        raise HTTPException(
            HTTPStatus.NOT_FOUND,
            f"Requested item /item/{id} was not found",
        )
    return ItemResponse.from_entity(entity)


@router.get("/", response_model=List[ItemResponse])
async def get_item_list(
    offset: Annotated[NonNegativeInt, Query()] = 0,
    limit: Annotated[PositiveInt, Query()] = 10,
    min_price: Annotated[NonNegativeFloat | None, Query()] = None,
    max_price: Annotated[NonNegativeFloat | None, Query()] = None,
    show_deleted: Annotated[bool, Query()] = False,
) -> list[ItemResponse]:
    return [
        ItemResponse.from_entity(e)
        for e in storage.list_items(
            offset=offset,
            limit=limit,
            min_price=min_price,
            max_price=max_price,
            show_deleted=show_deleted,
        )
    ]


@router.put("/{id}", response_model=ItemResponse)
async def replace_item(id: int, item: ItemRequest) -> ItemResponse:
    entity = storage.replace_item(id, item.as_item_info())
    if not entity:
        raise HTTPException(
            HTTPStatus.NOT_FOUND, f"Item with id /item/{id} not found for replacement"
        )
    return ItemResponse.from_entity(entity)


@router.patch(
    "/{id}",
    response_model=ItemResponse,
    responses={
        HTTPStatus.OK: {
            "description": "Successfully patched item",
        },
        HTTPStatus.NOT_MODIFIED: {
            "description": "Failed to modify item as one was not found",
        },
    },
)
async def update_item(id: int, item: ItemPatchRequest) -> ItemResponse:
    entity = storage.patch_item(id, item.model_dump())
    if not entity:
        raise HTTPException(
            HTTPStatus.NOT_MODIFIED, f"Item with id /item/{id} not found for update"
        )
    return ItemResponse.from_entity(entity)


@router.delete("/{id}")
async def delete_item(id: int) -> Response:
    success = storage.delete_item(id)
    if not success:
        raise HTTPException(
            HTTPStatus.NOT_FOUND, f"Item with id /item/{id} not found for deletion"
        )
    return Response(status_code=HTTPStatus.OK)
