import json
from typing import Iterable, Optional
from pathlib import Path
from lecture_2.hw.shop_api.storage.item_model import ItemEntity, ItemInfo
from itertools import count

DATA_FILE_PATH = Path("./lecture_2/hw/shop_api/storage/item.json")

_id_generator = 0


def _load_data() -> dict[int, ItemInfo]:
    global _id_generator
    if DATA_FILE_PATH.exists():
        with DATA_FILE_PATH.open("r") as file:
            result_dict = {int(k): ItemInfo(**v) for k, v in json.load(file).items()}
            _id_generator = max(int(k) for k in result_dict) if result_dict else 0

            return result_dict

    return {}


def _save_data() -> None:
    with DATA_FILE_PATH.open("w") as file:
        json.dump({k: v.to_dict() for k, v in _data.items()}, file, indent=4)


# Initialize in-memory data store
_data = _load_data()


def add_item(info: ItemInfo) -> ItemEntity:
    global _id_generator
    _id_generator += 1
    _id = _id_generator

    _data[_id] = info
    _save_data()
    return ItemEntity(_id, info)


def get_item_by_id(id: int) -> Optional[ItemEntity]:
    if id in _data and not _data[id].deleted:
        return ItemEntity(id, _data[id])
    return None


def list_items(
    offset: int = 0,
    limit: int = 10,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    show_deleted: bool = False,
) -> Iterable[ItemEntity]:
    filtered_items = [
        ItemEntity(item_id, item_info)
        for item_id, item_info in _data.items()
        if (
            (show_deleted or not item_info.deleted)
            and (min_price is None or item_info.price >= min_price)
            and (max_price is None or item_info.price <= max_price)
        )
    ]
    return filtered_items[offset : offset + limit]


def replace_item(id: int, info: ItemInfo) -> Optional[ItemEntity]:
    if id in _data:
        _data[id] = info
        _save_data()
        return ItemEntity(id, info)
    return None


def patch_item(id: int, patch_data: dict) -> Optional[ItemEntity]:
    if id not in _data or _data[id].deleted:
        return None

    _data[id].name = (
        patch_data["name"] if not patch_data["name"] == None else _data[id].name
    )
    _data[id].price = (
        patch_data["price"] if not patch_data["price"] == None else _data[id].price
    )

    _save_data()
    return ItemEntity(id, _data[id])


def delete_item(id: int) -> bool:
    if id in _data:
        _data[id].deleted = True
        _save_data()
        return True
    return False
