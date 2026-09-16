"""Stage 3: persist fictional products, stock and orders in SQLite."""

import os
import sqlite3
from pathlib import Path

from menu import MENU
from ordering import validate_order_input


# Keep the database beside this file, regardless of the terminal's folder.
DATABASE_PATH = Path(os.environ.get("TAKEAWAY_DATABASE_PATH", str(Path(__file__).resolve().with_name("restaurant.db"))))
INITIAL_STOCK = {
    1: 20, 2: 30, 3: 15, 4: 20, 5: 20, 6: 15,
    7: 25, 8: 25, 9: 15, 10: 40, 11: 40, 12: 20,
}


class ItemNotFoundError(ValueError):
    """Requested product does not exist."""


class InsufficientStockError(ValueError):
    """Requested quantity exceeds available stock."""


def connect(database_path=DATABASE_PATH):
    connection = sqlite3.connect(database_path)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def initialise_database(database_path=DATABASE_PATH):
    connection = connect(database_path)
    try:
        with connection:
            connection.execute("""
                CREATE TABLE IF NOT EXISTS products (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    price_pence INTEGER NOT NULL CHECK(price_pence >= 0),
                    stock INTEGER NOT NULL CHECK(stock >= 0)
                )
            """)
            connection.execute("""
                CREATE TABLE IF NOT EXISTS orders (
                    id INTEGER PRIMARY KEY,
                    item_id INTEGER NOT NULL REFERENCES products(id),
                    quantity INTEGER NOT NULL CHECK(quantity BETWEEN 1 AND 50),
                    total_pence INTEGER NOT NULL CHECK(total_pence >= 0),
                    status TEXT NOT NULL DEFAULT 'queued',
                    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
                )
            """)
            for item in MENU:
                connection.execute("""
                    INSERT INTO products (id, name, price_pence, stock)
                    VALUES (?, ?, ?, ?)
                    ON CONFLICT(id) DO NOTHING
                """, (item["id"], item["name"], item["price_pence"],
                      INITIAL_STOCK.get(item["id"], 0)))
    finally:
        connection.close()


def get_menu(database_path=DATABASE_PATH):
    connection = connect(database_path)
    try:
        rows = connection.execute(
            "SELECT * FROM products ORDER BY id"
        ).fetchall()
        return [dict(row) for row in rows]
    finally:
        connection.close()


def place_order(item_id, quantity, database_path=DATABASE_PATH):
    validate_order_input(item_id, quantity)
    connection = connect(database_path)
    try:
        with connection:
            # Reserve stock only when enough exists, in one SQL statement.
            result = connection.execute("""
                UPDATE products SET stock = stock - ?
                WHERE id = ? AND stock >= ?
            """, (quantity, item_id, quantity))

            if result.rowcount == 0:
                item = connection.execute(
                    "SELECT id FROM products WHERE id = ?", (item_id,)
                ).fetchone()
                if item is None:
                    raise ItemNotFoundError("Menu item not found.")
                raise InsufficientStockError("Insufficient stock.")

            item = connection.execute(
                "SELECT * FROM products WHERE id = ?", (item_id,)
            ).fetchone()
            total = item["price_pence"] * quantity
            result = connection.execute("""
                INSERT INTO orders (item_id, quantity, total_pence)
                VALUES (?, ?, ?)
            """, (item_id, quantity, total))
            order = {
                "order_id": result.lastrowid,
                "item_id": item_id,
                "name": item["name"],
                "quantity": quantity,
                "total_pence": total,
                "status": "queued",
            }
        # The transaction has committed before we report success.
        return order
    finally:
        connection.close()


def get_orders(database_path=DATABASE_PATH):
    connection = connect(database_path)
    try:
        rows = connection.execute("""
            SELECT orders.*, products.name
            FROM orders JOIN products ON orders.item_id = products.id
            ORDER BY orders.id
        """).fetchall()
        return [dict(row) for row in rows]
    finally:
        connection.close()
