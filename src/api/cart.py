from fastapi import Response, status, APIRouter
from src.db.memory import carts
from src.models.cart import Cart


cart_router = APIRouter(prefix="/v1")


@cart_router.post("/cart")
def add_items_to_cart(request: Cart):
    """
    Endpoint to add items to cart
    """

    # check if cart is empty for the user
    if request.user_id not in carts:
        carts[request.user_id] = Cart(user_id=request.user_id)

    # get existing list of cart items
    existing_items = {item.item_id for item in carts[request.user_id].items}

    # only add items which are not already in cart
    new_items = [item for item in request.items if item.item_id not in existing_items]

    # if user id already exists in card just extend the new items
    carts[request.user_id].items.extend(new_items)

    return Response(status_code=status.HTTP_201_CREATED)


@cart_router.get("/cart/{user_id}")
def view_cart(user_id: str):
    """
    Endpoint to view cart for a user
    """
    # check if user id exists in cart
    if user_id not in carts:
        return Response(status_code=status.HTTP_404_NOT_FOUND)

    return Response(status_code=status.HTTP_200_OK, content=carts[user_id].json())
