from fastapi import FastAPI

from .routes.cart import router as router_cart
from .routes.item import router as router_item

app = FastAPI(title="Shop API")

app.include_router(router_cart)
app.include_router(router_item)
