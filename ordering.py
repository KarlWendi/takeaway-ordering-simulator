"""Stage 2: validate and calculate a single-product order."""

from menu import MENU, display_menu, format_price


def find_item(item_id):
    """Find by product ID, regardless of the product's list position."""
    for item in MENU:
        if item["id"] == item_id:
            return item
    raise ValueError("Menu item not found.")


def validate_order_input(item_id, quantity):
    """Shared input rules for the quote and database stages."""
    if type(item_id) is not int or item_id <= 0:
        raise ValueError("Product ID must be a positive whole number.")
    if type(quantity) is not int or not 1 <= quantity <= 50:
        raise ValueError("Quantity must be a whole number from 1 to 50.")


def calculate_order(item_id, quantity):
    """Return order details without changing the menu or saving an order."""
    validate_order_input(item_id, quantity)
    item = find_item(item_id)
    return {
        "item_id": item["id"],
        "name": item["name"],
        "quantity": quantity,
        "total_pence": item["price_pence"] * quantity,
    }


def main():
    display_menu()
    try:
        item_id = int(input("Product ID: "))
        quantity = int(input("Quantity (1–50): "))
    except ValueError:
        print("Please enter whole numbers, such as 1 and 2.")
        return

    try:
        order = calculate_order(item_id, quantity)
    except ValueError as error:
        print(f"Order rejected: {error}")
        return

    total = format_price(order["total_pence"])
    print(f"Order summary: {order['quantity']} x {order['name']} = {total}")
    print("Simulation only: this order has not been saved or paid for.")


if __name__ == "__main__":
    main()
