from pydantic import BaseModel
from typing import List
from src.models.item import Item


class Cart(BaseModel):
    """
    Model to manage cart data
    """

    user_id: str
    items: List[Item] = []
