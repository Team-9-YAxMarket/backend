from typing import List, Optional

from pydantic import UUID4, BaseModel, PositiveInt

from src.api.request_models.item_request import ItemRequest


class OrderCreateRequest(BaseModel):
    items: List[ItemRequest]


class OrderUpdateRequest(BaseModel):
    items: List[ItemRequest]
    recommended_carton: List[Optional[str]]
