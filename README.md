# Takeaway Ordering Simulator

An educational Python project exploring food ordering, inventory and kitchen waiting times. Uses fictional data and is not affiliated with McDonald's or any other restaurant.

## Current stage: 1 — a menu in Python

Displays three products and formats integer prices in pence as pounds. No external packages are needed. Orders, stock tracking and an API are planned, not implemented yet.

## Run

With Python 3 installed, open a terminal in this folder:

```text
python menu.py
```

On Windows, `py menu.py` may work if the Python launcher is installed.

Expected output:

```text
Takeaway menu
1. Burger - £3.99
2. Fries - £1.99
3. Wrap - £4.49
```

## Development roadmap

- [x] Stage 1: menu, lists, dictionaries, functions and money formatting.
- [ ] Stage 2: look up products and calculate an order total; validate inputs.
- [ ] Stage 3: persist menu, stock and orders in SQLite; use transactions.
- [ ] Stage 4: expose ordering through a FastAPI API.
- [ ] Stage 5: simulate kitchen scheduling and compare waiting times.
- [ ] Stage 6: document experiments, meaningful tests and a demonstration.

Each stage will have its own commit and explanation. See [LEARNING.md](LEARNING.md) for the reasoning and exercises.

## Verification

Stage 1 was run with Python and its output checked. Price formatting was also checked at 0, 5, 100 and 399 pence.

## Limitations

The menu exists only in Python memory. There is no database, customer interface, payment processing or real restaurant integration.
