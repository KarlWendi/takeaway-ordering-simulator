# Takeaway Ordering Simulator

An educational Python project exploring food ordering, inventory and kitchen waiting times. Uses fictional data and is not affiliated with McDonald's or any other restaurant.

## Current stage: 3 — persistent orders and inventory

Displays the menu with current stock, saves orders in SQLite and reduces stock in the same transaction. Rejects missing products, invalid quantities and insufficient stock. Orders and stock survive a restart. No external packages are needed; sqlite3 is included with Python. An API and kitchen scheduling are planned, not implemented yet.

## Run

With Python 3 installed, open a terminal in this folder:

```text
python restaurant.py
```

On Windows, `py restaurant.py` may work if the Python launcher is installed. Earlier stages still run with `python menu.py` or `python ordering.py`. Keep all Python files in the same folder.

Example on a fresh database (the program also prints its database path):

```text
Takeaway menu — current stock
1. Burger - £3.99 (stock: 20)
2. Fries - £1.99 (stock: 30)
3. Wrap - £4.49 (stock: 15)
Saved orders: 0
Product ID (Enter to exit): 1
Quantity (1–50): 2
Saved order #1: 2 x Burger = £7.98
Stock updated. Simulation only; no payment taken.
```

## Development roadmap

- [x] Stage 1: menu, lists, dictionaries, functions and money formatting.
- [x] Stage 2: look up products and calculate an order total; validate inputs.
- [x] Stage 3: persist menu, stock and orders in SQLite; use transactions.
- [ ] Stage 4: expose ordering through a FastAPI API.
- [ ] Stage 5: simulate kitchen scheduling and compare waiting times.
- [ ] Stage 6: document experiments, meaningful tests and a demonstration.

Each stage will have its own commit and explanation. See [LEARNING.md](LEARNING.md) for the reasoning and exercises.

## Verification

Stage 1 was run with Python and its output checked. Price formatting was also checked at 0, 5, 100 and 399 pence.

Stage 2: six automated tests passed, covering totals, quantity boundaries, invalid quantities/IDs and lookup independent of list position. The terminal flow was checked with valid inputs, an unknown product, zero quantity and non-numeric input.

Stage 3: seven additional database tests passed, including persistence across new connections, reinitialisation without resetting stock, rejected orders and rollback when saving fails. All 13 tests passed together. A separate-process demonstration verified stock and orders survive restarting Python.

Run the tests from this folder:

```text
python -m unittest -v
```

## Limitations

There is no mixed-product basket, ingredient inventory, stock replenishment command, payment processing or real restaurant integration. Stock counts finished products. All saved orders remain queued until a later stage adds status changes. The maximum quantity of 50 is an invented demonstration rule.

## Database and files

`database.py` handles SQLite; `restaurant.py` handles the terminal. `ordering.py` supplies shared input validation, and `menu.py` supplies initial products and price formatting. `restaurant.db` is created automatically beside database.py on first run and is ignored by Git. Do not upload your database; someone cloning the code gets a fresh simulation.

Restart `restaurant.py` after placing two burgers: stock should be 18 and the saved order should appear. Press Enter at the product prompt to exit without ordering. Initial products are inserted only when their IDs are missing: editing menu.py does not overwrite existing database prices or reset stock. New products without an entry in INITIAL_STOCK start with zero stock.
