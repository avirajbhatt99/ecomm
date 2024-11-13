from fastapi import status, APIRouter, HTTPException
from fastapi.responses import JSONResponse
from src.models.order import Order
from src.models.discount_code import DiscountCode
from src.db.db_manager import DBManager
from src.utils.helper import Helper

order_router = APIRouter(prefix="/v1")

cart_storage = "src/db/temp/cart.json"
order_storage = "src/db/temp/order.json"
discount_storage = "src/db/temp/discount.json"

nth_order = 2


@order_router.post("/checkout")
def checkout(request: Order):
    """
    Endpoint to handle checkout
    """

    carts = DBManager.load(cart_storage)
    orders = DBManager.load(order_storage)
    orders_count = DBManager.count(order_storage)
    discount_codes = DBManager.load(discount_storage)

    if not discount_codes:
        discount_codes = {}

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
    total = Helper.calculate_total_amount(cart["items"])
    discount_applied = 0.0

    if request.discount_code:
        # check if discount code is valid
        valid_code = discount_codes.get(str(order_number), {}).get("code")

        if not valid_code == request.discount_code:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid discount code",
            )

        # apply discount to total amount
        discount_percentage = 0.1
        discount_applied = total * discount_percentage
        total -= discount_applied

    order_id = f"ORDER-{order_number}"
    order = Order(
        order_id=order_id,
        user_id=request.user_id,
        items=cart["items"],
        total_amount=total,
        discount_code=request.discount_code if discount_applied else None,
        discount_applied=discount_applied,
    )

    # store order in file storage and clear the cart for user
    orders.append(order.model_dump())

    carts[request.user_id]["items"] = []

    DBManager.save(order_storage, orders)
    DBManager.save(cart_storage, carts)

    return JSONResponse(
        content={"message": "Order placed successfully"}, status_code=status.HTTP_200_OK
    )


@order_router.get("/order/{user_id}")
def order_detail(user_id: str):
    """
    get order details of a user
    """

    carts = DBManager.load(cart_storage)
    orders_count = DBManager.count(order_storage)
    discount_codes = DBManager.load(discount_storage)

    if not discount_codes:
        discount_codes = {}

    # check if cart is empty
    if user_id not in carts or not carts[user_id]["items"]:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No order found",
        )

    cart = carts[user_id]

    order_number = orders_count + 1

    discount_code = discount_codes.get(str(order_number), {}).get("code")

    # create discount code for nth order, if not already generated
    if order_number % nth_order == 0 and discount_code is None:
        discount_code = f"DISCOUNT-{len(discount_codes) + 1}"
        discount_codes[order_number] = DiscountCode(
            code=discount_code, valid_for_order_number=order_number
        ).model_dump()

        DBManager.save(discount_storage, discount_codes)

    order_id = f"ORDER-{order_number}"
    total = Helper.calculate_total_amount(cart["items"])
    order = Order(
        order_id=order_id,
        user_id=user_id,
        items=cart["items"],
        total_amount=total,
        discount_code=discount_code,
    )

    return JSONResponse(content=order.model_dump(), status_code=status.HTTP_200_OK)
