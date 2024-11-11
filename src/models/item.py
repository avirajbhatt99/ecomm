from pydantic import BaseModel


class Item(BaseModel):
    """
    Model to manage items
    """

    item_id: str
    quantity: int
    price: float
