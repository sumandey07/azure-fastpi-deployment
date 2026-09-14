"""In-memory item store used as a simple example backend.

Swap this out for a real database (e.g. Azure Cosmos DB or Azure SQL)
in production.
"""
from itertools import count
from threading import Lock

from app.schemas import Item, ItemCreate, ItemUpdate


class ItemStore:
    def __init__(self) -> None:
        self._items: dict[int, Item] = {}
        self._ids = count(1)
        self._lock = Lock()

    def list(self) -> list[Item]:
        return list(self._items.values())

    def get(self, item_id: int) -> Item | None:
        return self._items.get(item_id)

    def create(self, data: ItemCreate) -> Item:
        with self._lock:
            item_id = next(self._ids)
            item = Item(id=item_id, **data.model_dump())
            self._items[item_id] = item
            return item

    def update(self, item_id: int, data: ItemUpdate) -> Item | None:
        with self._lock:
            existing = self._items.get(item_id)
            if existing is None:
                return None
            updated = existing.model_copy(
                update=data.model_dump(exclude_unset=True)
            )
            self._items[item_id] = updated
            return updated

    def delete(self, item_id: int) -> bool:
        with self._lock:
            return self._items.pop(item_id, None) is not None


store = ItemStore()
