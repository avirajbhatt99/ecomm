from pydantic import BaseModel, Field
from typing import List, Optional
from src.models.item import Item


class Order(BaseModel):
    order_id: Optional[str] = None
    user_id: str
    items: Optional[List[Item]] = None
    total_amount: Optional[float] = None
    discount_code: Optional[str] = None
    discount_applied: Optional[float] = None
