"""Stage 4: run with python -m uvicorn api:app --reload."""

from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, ConfigDict, Field

from database import (
    DATABASE_PATH, InsufficientStockError, ItemNotFoundError,
    get_menu, get_orders, initialise_database, place_order,
)


class OrderRequest(BaseModel):
    """Define and validate the JSON a client must send."""
    model_config = ConfigDict(extra="forbid")
    item_id: int = Field(strict=True, gt=0)
    quantity: int = Field(strict=True, ge=1, le=50)


def create_app(database_path=DATABASE_PATH):
    """Tests can supply a temporary database instead of the user's data."""
    @asynccontextmanager
    async def lifespan(application):
        initialise_database(database_path)
        yield

    application = FastAPI(
        title="Takeaway Ordering Simulator",
        description="Educational mock API using fictional data; no payments.",
        version="0.4.0",
        lifespan=lifespan,
    )

    @application.get("/")
    def home():
        return {"message": "Takeaway mock API", "documentation": "/docs"}

    @application.get("/menu")
    def menu_endpoint():
        return get_menu(database_path)

    @application.get("/orders")
    def orders_endpoint():
        return get_orders(database_path)

    @application.post("/orders", status_code=201)
    def order_endpoint(order: OrderRequest):
        try:
            return place_order(order.item_id, order.quantity, database_path)
        except ItemNotFoundError as error:
            raise HTTPException(status_code=404, detail=str(error)) from error
        except InsufficientStockError as error:
            raise HTTPException(status_code=409, detail=str(error)) from error

    return application


app = create_app()
