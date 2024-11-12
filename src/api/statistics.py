from fastapi import status, APIRouter
from fastapi.responses import JSONResponse
from src.db.db_manager import DBManager
from src.utils.helper import Helper


statistics_router = APIRouter(prefix="/v1")

order_storage = "src/db/temp/order.json"
discount_storage = "src/db/temp/discount.json"


@statistics_router.get("/statistics")
def get_statistics():
    """
    Endpoint to get statistics
    """
    orders = DBManager.load(order_storage)
    discount_codes = DBManager.load(discount_storage)

    if not discount_codes:
        discount_codes = {}

    if not orders:
        orders = {}

    statistics = {}
    statistics["items_purchsed"] = Helper.get_items_purchased_count(orders)
    statistics["total_amount"] = Helper.get_total_amount(orders)
    statistics["discount_amount"] = Helper.get_discount_amount(orders)
    statistics["discount_codes"] = Helper.get_discount_codes(discount_codes)

    return JSONResponse(content=statistics, status_code=status.HTTP_200_OK)
