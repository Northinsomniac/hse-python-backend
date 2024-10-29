from dataclasses import dataclass


@dataclass(slots=True)
class ItemInfo:
    name: str
    price: float
    deleted: bool

    def to_dict(self):
        return {"name": self.name, "price": self.price, "deleted": self.deleted}


@dataclass(slots=True)
class ItemEntity:
    id: int
    info: ItemInfo

    def to_dict(self):
        return {"id": self.id, "info": self.info.to_dict()}


@dataclass(slots=True)
class ItemPatchInfo:

    name: str | None = None
    price: float | None = None

    def to_dict(self):
        return {"name": self.name, "price": self.price}


# @dataclass(slots=True)
# class DeleteItemInfo:
#     name: str | None = None
#     published: bool | None = None
