from fastapi.testclient import TestClient
from src.server import app
from src.models.cart import Cart
from src.models.item import Item
from src.db.db_manager import DBManager
from src.tests.utils import empty_cart

client = TestClient(app)


def test_add_items_to_cart():
    user_id = "234"

    # empty cart
    empty_cart(user_id)

    cart_items = [
        Item(item_id="item1", quantity=2, price=20),
        Item(item_id="item2", quantity=1, price=25),
    ]

    # create request data
    request_data = Cart(user_id=user_id, items=cart_items)

    # get response
    response = client.post("/v1/cart", json=request_data.model_dump())

    assert response.status_code == 201
    assert response.json() == {"message": "Items added to cart"}

    carts = DBManager.load("src/db/temp/cart.json")
    assert user_id in carts
    assert len(carts[user_id]["items"]) == 2

    # empty cart
    empty_cart(user_id)
