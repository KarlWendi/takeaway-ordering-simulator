"""Run this file for Stage 3's persistent ordering demonstration."""

from database import (
    DATABASE_PATH, get_menu, get_orders, initialise_database, place_order,
)
from menu import format_price


def main():
    initialise_database()
    print(f"Database: {DATABASE_PATH}")
    print("Takeaway menu — current stock")
    for item in get_menu():
        price = format_price(item["price_pence"])
        print(f"{item['id']}. {item['name']} - {price} "
              f"(stock: {item['stock']})")

    orders = get_orders()
    print(f"Saved orders: {len(orders)}")
    for order in orders:
        print(f"#{order['id']}: {order['quantity']} x {order['name']} "
              f"= {format_price(order['total_pence'])} ({order['status']})")

    raw_id = input("Product ID (Enter to exit): ").strip()
    if not raw_id:
        return
    try:
        item_id = int(raw_id)
        quantity = int(input("Quantity (1–50): "))
    except ValueError:
        print("Please enter whole numbers.")
        return
    try:
        order = place_order(item_id, quantity)
    except ValueError as error:
        print(f"Order rejected: {error}")
        return

    print(f"Saved order #{order['order_id']}: {order['quantity']} x "
          f"{order['name']} = {format_price(order['total_pence'])}")
    print("Stock updated. Simulation only; no payment taken.")


if __name__ == "__main__":
    main()
