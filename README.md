# Takeaway Ordering Simulator

An educational Python project exploring food ordering, inventory and kitchen waiting times. Uses fictional data and is not affiliated with McDonald's or any other restaurant.

## Current stage: 2 — order calculation and validation

Displays three products, accepts a product ID and quantity, and calculates an order summary. Rejects missing products and invalid quantities. No external packages are needed. Database persistence, stock tracking and an API are planned, not implemented yet.

## Run

With Python 3 installed, open a terminal in this folder:

```text
python ordering.py
```

On Windows, `py ordering.py` may work if the Python launcher is installed. To display only the stage-1 menu, run `python menu.py`.

Expected output:

```text
Takeaway menu
1. Burger - £3.99
2. Fries - £1.99
3. Wrap - £4.49
Product ID: 1
Quantity (1–50): 2
Order summary: 2 x Burger = £7.98
Simulation only: this order has not been saved or paid for.
```

## Development roadmap

- [x] Stage 1: menu, lists, dictionaries, functions and money formatting.
- [x] Stage 2: look up products and calculate an order total; validate inputs.
- [ ] Stage 3: persist menu, stock and orders in SQLite; use transactions.
- [ ] Stage 4: expose ordering through a FastAPI API.
- [ ] Stage 5: simulate kitchen scheduling and compare waiting times.
- [ ] Stage 6: document experiments, meaningful tests and a demonstration.

Each stage will have its own commit and explanation. See [LEARNING.md](LEARNING.md) for the reasoning and exercises.

## Verification

Stage 1 was run with Python and its output checked. Price formatting was also checked at 0, 5, 100 and 399 pence.

Stage 2: six automated tests passed, covering totals, quantity boundaries, invalid quantities/IDs and lookup independent of list position. The terminal flow was checked with valid inputs, an unknown product, zero quantity and non-numeric input.

Run the tests from this folder:

```text
python -m unittest -v
```

## Limitations

The menu and calculated order exist only in Python memory. There is a terminal interface but no database, mixed-product basket, stock check, payment processing or real restaurant integration. The maximum quantity of 50 is an invented demonstration rule.
