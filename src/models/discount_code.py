from pydantic import BaseModel


class DiscountCode(BaseModel):
    """
    Model to manage discount code
    """

    code: str
    valid_for_order_number: int
