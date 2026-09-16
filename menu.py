"""Stage 1: display a fictional takeaway menu. Run with Python 3."""

MENU = [
    {"id": 1, "name": "Burger", "price_pence": 399},
    {"id": 2, "name": "Fries", "price_pence": 199},
    {"id": 3, "name": "Wrap", "price_pence": 449},
]


def format_price(pence):
    """Turn an integer number of pence into pounds for display."""
    pounds, remaining_pence = divmod(pence, 100)
    return f"£{pounds}.{remaining_pence:02d}"


def display_menu():
    """Print one line for each menu item."""
    print("Takeaway menu")
    for item in MENU:
        price = format_price(item["price_pence"])
        print(f"{item['id']}. {item['name']} - {price}")


if __name__ == "__main__":
    display_menu()
