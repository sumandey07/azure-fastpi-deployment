"""Item CRUD routes."""
from fastapi import APIRouter, HTTPException, status

from app.schemas import Item, ItemCreate, ItemUpdate
from app.store import store

router = APIRouter(prefix="/items", tags=["items"])


@router.get("", response_model=list[Item])
async def list_items() -> list[Item]:
    return store.list()


@router.post("", response_model=Item, status_code=status.HTTP_201_CREATED)
async def create_item(payload: ItemCreate) -> Item:
    return store.create(payload)


@router.get("/{item_id}", response_model=Item)
async def get_item(item_id: int) -> Item:
    item = store.get(item_id)
    if item is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Item not found")
    return item


@router.patch("/{item_id}", response_model=Item)
async def update_item(item_id: int, payload: ItemUpdate) -> Item:
    item = store.update(item_id, payload)
    if item is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Item not found")
    return item


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(item_id: int) -> None:
    if not store.delete(item_id):
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Item not found")
