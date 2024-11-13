from fastapi.testclient import TestClient
from src.server import app
from src.models.cart import Cart
from src.models.item import Item
from src.db.db_manager import DBManager
from src.tests.utils import empty_cart


client = TestClient(app)

order_storage = "src/db/temp/order.json"


def test_get_order_details_success():

    user_id = "234"

    # empty cart
    empty_cart(user_id)

    cart_items = [
        Item(item_id="item1", quantity=2, price=20),
        Item(item_id="item2", quantity=1, price=25),
    ]
    request_data = Cart(user_id=user_id, items=cart_items)

    # add items to cart
    client.post("/v1/cart", json=request_data.model_dump())

    # get order details
    response = client.get(f"/v1/order/{user_id}")

    assert response.status_code == 200
    order_data = response.json()
    assert order_data["user_id"] == user_id
    assert len(order_data["items"]) == 2
    assert order_data["total_amount"] == 65

    # empty cart
    empty_cart(user_id)


def test_checkout_success():
    user_id = "234"

    # empty cart
    empty_cart(user_id)

    cart_items = [
        Item(item_id="item3", quantity=2, price=20),
        Item(item_id="item4", quantity=1, price=25),
    ]
    request_data = Cart(user_id=user_id, items=cart_items)

    # add items to cart
    client.post("/v1/cart", json=request_data.model_dump())

    checkout_data = {"user_id": user_id}
    # checkout
    response = client.post(f"/v1/checkout", json=checkout_data)

    assert response.status_code == 200
    order_data = response.json()
    assert order_data["message"] == "Order placed successfully"

    # empty cart
    empty_cart(user_id)


def test_get_order_details_with_discount_coupon():
    user_id = "234"
    # empty cart
    empty_cart(user_id)
    cart_items = [
        Item(item_id="item5", quantity=2, price=20),
        Item(item_id="item6", quantity=1, price=25),
    ]
    request_data = Cart(user_id=user_id, items=cart_items)

    # add items to cart
    client.post("/v1/cart", json=request_data.model_dump())

    orders_count = DBManager.count(order_storage)

    order_number = orders_count + 1

    # get order details
    response = client.get(f"/v1/order/{user_id}")

    assert response.status_code == 200
    order_data = response.json()
    assert order_data["user_id"] == user_id
    assert len(order_data["items"]) == 2
    assert order_data["total_amount"] == 65
    if order_number % 2 == 0:
        assert order_data["discount_code"] is not None
    else:
        assert order_data["discount_code"] is None

    # empty cart
    empty_cart(user_id)


def test_checkout_success_with_discount_code():
    user_id = "234"

    # empty cart
    empty_cart(user_id)

    cart_items = [
        Item(item_id="item7", quantity=2, price=20),
        Item(item_id="item8", quantity=1, price=25),
    ]
    request_data = Cart(user_id=user_id, items=cart_items)

    # add items to cart
    client.post("/v1/cart", json=request_data.model_dump())

    orders_count = DBManager.count(order_storage)

    order_number = orders_count + 1

    discount_code = None
    if order_number % 2 == 0:
        discount_code = f"DISCOUNT-{int(order_number/2)}"

    checkout_data = {"user_id": user_id}

    if discount_code:
        checkout_data["discount_code"] = discount_code

    # checkout
    response = client.post(f"/v1/checkout", json=checkout_data)

    assert response.status_code == 200
    order_data = response.json()
    assert order_data["message"] == "Order placed successfully"

    # empty cart
    empty_cart(user_id)


def test_get_order_details_not_found():
    user_id = "234"

    # empty cart
    empty_cart(user_id)
    response = client.get(f"/v1/order/{user_id}")
    assert response.status_code == 404
    assert response.json() == {"detail": "No order found"}

    # empty cart
    empty_cart(user_id)


def test_invalid_discount_code():
    user_id = "234"

    # empty cart
    empty_cart(user_id)
    cart_items = [
        Item(item_id="item9", quantity=2, price=20),
        Item(item_id="item10", quantity=1, price=25),
    ]
    request_data = Cart(user_id=user_id, items=cart_items)

    # add items to cart
    client.post("/v1/cart", json=request_data.model_dump())

    orders_count = DBManager.count(order_storage)

    order_number = orders_count + 1

    discount_code = f"INVALID-DISCOUNT-{int(order_number/2)}"

    checkout_data = {"user_id": user_id, "discount_code": discount_code}

    # checkout
    response = client.post(f"/v1/checkout", json=checkout_data)

    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid discount code"}

    # empty cart
    empty_cart(user_id)
