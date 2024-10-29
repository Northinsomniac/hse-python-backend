from __future__ import annotations

from pydantic import BaseModel, ConfigDict

from typing_extensions import List
from lecture_2.hw.shop_api.storage.item_model import ItemEntity, ItemInfo, ItemPatchInfo


class ItemResponse(BaseModel):
    """Contract model where we build items return to User."""

    id: int
    name: str
    price: float = 0.0
    deleted: bool

    @staticmethod
    def from_entity(entity: ItemEntity) -> ItemResponse:
        """Convert DB models into network's version."""
        return ItemResponse(
            id=entity.id,
            name=entity.info.name,
            price=float(entity.info.price),
            deleted=entity.info.deleted,
        )


class ItemRequest(BaseModel):
    """Contract we use to create another item."""

    name: str
    price: float = 0.0
    deleted: bool = False

    def as_item_info(self) -> ItemInfo:
        return ItemInfo(name=self.name, price=float(self.price), deleted=self.deleted)


class ItemPatchRequest(BaseModel):
    """Contract we use to path item."""

    name: str | None = None
    price: float | None = None

    model_config = ConfigDict(extra="forbid")

    def as_item_patch_info(self) -> ItemPatchInfo:
        return ItemPatchInfo(name=self.name, price=float(self.price))
