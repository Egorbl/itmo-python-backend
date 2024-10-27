from typing import List, Optional

from pydantic import BaseModel, Field, TypeAdapter, Extra


class Item(BaseModel):
    id : int
    name: str
    price: float
    deleted: bool

class CreateItemRequest(BaseModel):
    name: str
    price: float = Field(..., ge=0)

class PatchItemRequest(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None

    model_config = {
        "extra": "forbid"  # Запрещаем любые дополнительные параметры
    }


class Cart(BaseModel):
    id : int

CartList = TypeAdapter(List[Cart])