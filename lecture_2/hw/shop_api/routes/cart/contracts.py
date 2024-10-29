from __future__ import annotations
from typing_extensions import List
from pydantic import BaseModel, ConfigDict

from lecture_2.hw.shop_api.storage.cart_model import CartItemInfo, CartEntity


class CartResponse(BaseModel):
    """Contract model, where we build Carts return to User."""

    id: int
    items: List[CartItemInfo]
    price: float

    @staticmethod
    def from_entity(entity: CartEntity) -> CartResponse:
        """Convert DB models into network's version."""
        return CartResponse(
            id=entity.id, items=entity.info.items, price=entity.info.price
        )
