import json
from fastapi import status, APIRouter
from fastapi.responses import JSONResponse
from src.db.db_manager import DBManager
from src.models.cart import Cart
from src.utils.helper import Helper

cart_storage = "src/db/temp/cart.json"

cart_router = APIRouter(prefix="/v1")


@cart_router.post("/cart")
def add_items_to_cart(request: Cart):
    """
    Endpoint to add items to cart
    """

    carts = DBManager.load(cart_storage)

    if not carts:
        carts = {}

    # check if cart is empty for the user
    if request.user_id not in carts:
        carts[request.user_id] = Cart(user_id=request.user_id).model_dump()

    # get existing list of cart items
    existing_items = {item["item_id"] for item in carts[request.user_id]["items"]}

    # only add items which are not already in cart
    new_items = [
        item.model_dump()
        for item in request.items
        if item.item_id not in existing_items
    ]

    # if user id already exists in card just extend the new items
    carts[request.user_id]["items"].extend(new_items)

    DBManager.save(cart_storage, carts)

    return JSONResponse(
        content={"message": "Items added to cart"}, status_code=status.HTTP_201_CREATED
    )


@cart_router.get("/cart/{user_id}")
def view_cart(user_id: str):
    """
    Endpoint to view cart for a user
    """

    carts = DBManager.load(cart_storage)

    if not carts:
        carts = {}

    # check if user id exists in cart
    if user_id not in carts:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND)

    cart_data = carts[user_id]

    # calculate cart total
    total_amount = Helper.calculate_total_amount(cart_data["items"])

    cart_data["total_amount"] = total_amount

    return JSONResponse(status_code=status.HTTP_200_OK, content=cart_data)
