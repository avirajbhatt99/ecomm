import uvicorn
from fastapi import FastAPI
from src.db.db_manager import DBManager
from src.api.health import health_router
from src.api.cart import cart_router
from src.api.order import order_router
from src.api.statistics import statistics_router


app = FastAPI()

app.include_router(health_router)
app.include_router(cart_router)
app.include_router(order_router)
app.include_router(statistics_router)

# initialize db on
DBManager.initialize()

if __name__ == "__main__":
    uvicorn.run("src.server:app", host="0.0.0.0", port=8000, reload=True)
