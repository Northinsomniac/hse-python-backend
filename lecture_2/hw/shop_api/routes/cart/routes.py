from http import HTTPStatus
from typing import Annotated
from typing_extensions import List

from fastapi import APIRouter, HTTPException, Query, Response
from pydantic import NonNegativeInt, PositiveInt, PositiveFloat, NonNegativeFloat

from lecture_2.hw.shop_api.storage import cart_query as storage
from lecture_2.hw.shop_api.routes.cart.contracts import CartResponse

router = APIRouter(prefix="/cart")


@router.get(
    "/{id}",
    responses={
        HTTPStatus.OK: {
            "description": "Successfully returned requested cart",
        },
        HTTPStatus.NOT_FOUND: {
            "description": "Failed to return requested cart as one was not found",
        },
    },
)
async def get_cart_by_id(id: int) -> CartResponse:
    entity = storage.get_cart(id)  # returns CartEntity

    if not entity:
        raise HTTPException(
            HTTPStatus.NOT_FOUND,
            f"Request resource /cart/{id} was not found",
        )

    return CartResponse.from_entity(entity)


@router.get("/", response_model=List[CartResponse])
async def get_cart_list(
    offset: Annotated[NonNegativeInt, Query()] = 0,
    limit: Annotated[PositiveInt, Query()] = 10,
    min_price: Annotated[PositiveFloat | None, Query()] = None,
    max_price: Annotated[PositiveFloat | None, Query()] = None,
    min_quantity: Annotated[NonNegativeInt | None, Query()] = None,
    max_quantity: Annotated[NonNegativeInt | None, Query()] = None,
) -> list[CartResponse]:
    return [
        CartResponse.from_entity(e)
        for e in storage.get_all_carts(
            offset=offset,
            limit=limit,
            min_price=min_price,
            max_price=max_price,
            min_quantity=min_quantity,
            max_quantity=max_quantity,
        )
    ]


@router.post("/", status_code=HTTPStatus.CREATED, response_model=CartResponse)
async def post_cart(response: Response) -> CartResponse:
    entity = storage.add_cart()
    response.headers["location"] = f"/cart/{entity.id}"
    return CartResponse.from_entity(entity)


@router.put("/{cart_id}/add/{item_id}", response_model=CartResponse)
async def put_item_into_cart(
    cart_id: int, item_id: int, quantity: Annotated[PositiveInt, Query()] = 1
) -> CartResponse:
    entity = storage.add_item_to_cart(cart_id, item_id, quantity)
    if not entity:
        raise HTTPException(
            HTTPStatus.NOT_FOUND, f"Cart {cart_id} or item {item_id} not found."
        )
    return CartResponse.from_entity(entity)
