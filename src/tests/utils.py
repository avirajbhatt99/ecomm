from src.db.db_manager import DBManager


def empty_cart(user_id: str):
    """
    helper function to empty cart
    """
    cart_storage = "src/db/temp/cart.json"
    carts = DBManager.load(cart_storage)

    if not carts:
        carts = {}
    if user_id in carts:
        carts[user_id]["items"] = []
        DBManager.save(cart_storage, carts)
