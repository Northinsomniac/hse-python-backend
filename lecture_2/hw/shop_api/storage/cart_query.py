import json
from typing import Iterable, Optional
from pathlib import Path

from lecture_2.hw.shop_api.storage.cart_model import (
    CartEntity,
    CartInfo,
    CartItemInfo,
)

DATA_FILE_PATH = Path("./lecture_2/hw/shop_api/storage/cart.json")
ITEMS_FILE_PATH = Path("./lecture_2/hw/shop_api/storage/item.json")

_id_generator = 0


def _load_data() -> dict:
    global _id_generator
    if DATA_FILE_PATH.exists():
        with DATA_FILE_PATH.open("r") as file:
            result_dict = {int(k): CartInfo(**v) for k, v in json.load(file).items()}
            _id_generator = max(int(k) for k in result_dict) if result_dict else 0

            return result_dict

    return {}


def _load_items() -> dict:
    if ITEMS_FILE_PATH.exists():
        with ITEMS_FILE_PATH.open("r") as file:
            return {int(k): v for k, v in json.load(file).items()}
    return {}


def _save_data(data: dict) -> None:
    with DATA_FILE_PATH.open("w") as file:
        json.dump({k: v.to_dict() for k, v in data.items()}, file, indent=4)


_data = _load_data()


def add_cart() -> CartEntity:
    info = CartInfo(items=[], price=0)
    global _id_generator
    _id_generator += 1
    cart_id = _id_generator

    _data[cart_id] = info
    _save_data(_data)
    return CartEntity(cart_id, info)


def delete_cart(cart_id: int) -> None:
    if cart_id in _data:
        del _data[cart_id]
        _save_data(_data)


def get_cart(cart_id: int) -> Optional[CartEntity]:
    if cart_id not in _data:
        return None
    return CartEntity(cart_id, _data[cart_id])


def get_all_carts(
    offset: int = 0,
    limit: int = 10,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    min_quantity: Optional[int] = None,
    max_quantity: Optional[int] = None,
) -> Iterable[CartEntity]:
    filtered_carts = [
        CartEntity(cart_id, cart_info)
        for cart_id, cart_info in _data.items()
        if (
            (min_price is None or cart_info.price >= min_price)
            and (max_price is None or cart_info.price <= max_price)
            and (
                min_quantity is None
                or sum(item.quantity for item in cart_info.items) >= min_quantity
            )
            and (
                max_quantity is None
                or sum(item.quantity for item in cart_info.items) <= max_quantity
            )
        )
    ]

    paginated_carts = filtered_carts[offset : offset + limit]

    return paginated_carts


def update_cart(cart_id: int, info: CartInfo) -> Optional[CartEntity]:
    if cart_id not in _data:
        return None
    _data[cart_id] = info
    _save_data(_data)
    return CartEntity(cart_id, info)


def upsert_cart(cart_id: int, info: CartInfo) -> CartEntity:
    _data[cart_id] = info
    _save_data(_data)
    return CartEntity(cart_id, info)


def add_item_to_cart(
    cart_id: int, item_id: int, quantity: int = 1
) -> Optional[CartEntity]:
    if cart_id not in _data:
        return None

    items = _load_items()
    print(items)
    if item_id not in items:
        return None

    item_data = items[item_id]
    cart = _data[cart_id]

    match = False
    for item in cart.items:
        if item["id"] == item_id:
            item["quantity"] += quantity
            match = True
            break

    if not match:
        item_entity = CartItemInfo(
            id=item_id,
            name=item_data["name"],
            quantity=quantity,
            available=not item_data["deleted"]
        )
        cart.items.append(item_entity.to_dict())

    print(cart.items)
    cart.price = sum(
        item['quantity'] * items[item['id']]["price"] for item in cart.items
    )

    _save_data(_data)
    return CartEntity(cart_id, _data[cart_id])


def delete_item_from_cart(cart_id: int, item_id: int) -> Optional[CartEntity]:
    if cart_id not in _data:
        return None
    cart = _data[cart_id]
    cart.items = [item for item in cart.items if item.id != item_id]
    _save_data(_data)
    return CartEntity(cart_id, cart)


def update_item_in_cart(
    cart_id: int, item_id: int, item_info: CartItemInfo
) -> Optional[CartEntity]:
    if cart_id not in _data:
        return None
    cart = _data[cart_id]
    for item in cart.items:
        if item.id == item_id:
            item.info = item_info
            _save_data(_data)
            return CartEntity(cart_id, cart)
    return None
