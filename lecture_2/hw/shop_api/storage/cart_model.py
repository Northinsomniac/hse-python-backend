from dataclasses import dataclass
from typing_extensions import List


@dataclass(slots=True)
class CartItemInfo:
    id: int
    name: str
    quantity: int
    available: bool
    
    def to_dict(self):
        return {
            "id":self.id,
            "name": self.name,
            "quantity": self.quantity,
            "available": self.available
        }


@dataclass(slots=True)
class CartInfo:
    items: List[CartItemInfo]
    price: float
    
    def to_dict(self):
        return {
            "items": [item for item in self.items],
            "price": self.price
        }

@dataclass(slots=True)
class CartEntity:
    id: int
    info: CartInfo
    
    def to_dict(self):
        return {
            "id": self.id,
            "info": self.info.to_dict()
        }
