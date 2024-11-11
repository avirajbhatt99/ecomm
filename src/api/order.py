from fastapi import Response, status, APIRouter, HTTPException
from src.models.order import Order
from src.models.discount_code import DiscountCode
from src.db.db_manager import DBManager
from src.api.cart import cart_storage

order_router = APIRouter(prefix="/v1")

order_storage = "src/db/order.json"
discount_storage = "src/db/discount.json"

nth_order = 5


@order_router.post("/checkout/")
def checkout(request: Order):
    """
    Endpoint to handle checkout
    """

    carts = DBManager.load(cart_storage)
    orders = DBManager.load(order_storage)
    orders_count = DBManager.count(order_storage)
    discount_codes = DBManager.load(discount_storage)

    if not discount_codes:
        discount_codes = []

    if not orders:
        orders = []

    order_number = orders_count + 1

    # check if cart is empty
    if request.user_id not in carts or not carts[request.user_id]["items"]:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cart is empty",
        )

    # get cart items and calculate total amount
    cart = carts[request.user_id]
    total = sum(item["price"] * item["quantity"] for item in cart["items"])
    discount_applied = 0.0

    if request.discount_code:
        # check if discount code is valid
        valid = any(
            discount_code == request.discount_code
            and discount_code.valid_for_order_number == order_number
            for discount_code in discount_codes
        )

        if valid:

            # apply discount to total amount
            discount_percentage = 0.1
            discount_applied = total * discount_percentage
            total -= discount_applied

    order_id = f"ORDER-{order_number}"
    order = Order(
        order_id=order_id,
        user_id=request.user_id,
        items=request.items,
        total_amount=total,
        discount_code=request.discount_code if discount_applied else None,
        discount_applied=discount_applied,
    )

    # store order in file storage and clear the cart for user
    orders.append(order.model_dump())
    carts[request.user_id]["items"] = []

    DBManager.save(order_storage, orders)
    DBManager.save(cart_storage, carts)

    # if order was nth order, generate discount code for next nth order
    if order_number % nth_order == 0:
        discount_code = DiscountCode(code=f"DISCOUNT-{len(discount_codes) + 1}")
        discount_codes.append(
            DiscountCode(
                code=discount_code,
                valid_for_order_number=order_number + nth_order,
            )
        )

    return Response("Order placed successfully", status_code=status.HTTP_200_OK)
