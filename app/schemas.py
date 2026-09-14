"""Pydantic schemas for the API."""
from datetime import datetime, timezone
from pydantic import BaseModel, Field


class ItemBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, examples=["Widget"])
    description: str | None = Field(None, max_length=500)
    price: float = Field(..., gt=0, examples=[9.99])


class ItemCreate(ItemBase):
    pass


class ItemUpdate(BaseModel):
    name: str | None = Field(None, min_length=1, max_length=100)
    description: str | None = Field(None, max_length=500)
    price: float | None = Field(None, gt=0)


class Item(ItemBase):
    id: int
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class HealthResponse(BaseModel):
    status: str = "ok"
    service: str
    version: str
