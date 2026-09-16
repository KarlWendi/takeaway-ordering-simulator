# Demonstration guide

## Quick start for a reviewer

Download or clone this repository. Use Python 3.11 or newer and open a terminal in the repository folder. For an isolated environment on Windows:

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m unittest discover -v
.\.venv\Scripts\python.exe queue_demo.py
.\.venv\Scripts\python.exe -m uvicorn api:app --reload
```

On macOS/Linux, create the environment with `python3 -m venv .venv` and use `.venv/bin/python` in place of the Windows executable.

Keep Uvicorn running and open http://127.0.0.1:8000/docs. This is a local API testing page, not a public customer ordering website. GitHub does not run the server merely because the code is uploaded.

## Five-minute walkthrough

1. **Read the menu.** GET /menu → Try it out → Execute. Note burger stock. On a fresh database it is 20.
2. **Place one order.** POST /orders → Try it out → use `{"item_id": 1, "quantity": 2}` → Execute once. Expect 201, an order ID and total_pence 798 (£7.98).
3. **Check the effects.** GET /menu shows two fewer burgers; GET /orders lists the new order. Every successful POST creates another order, so do not treat repeated clicks as harmless refreshes.
4. **Reject invalid input.** POST quantity 0 → expect 422. POST item_id 999, quantity 1 → expect 404. Neither request creates an order or consumes stock.
5. **Compare capacity.** GET /queue with stations 1, 2 and 3. The result reads all currently queued orders. For a reproducible fixed workload, run queue_demo.py and compare the table in RESULTS.md.
6. **Show persistence.** Stop Uvicorn with Ctrl+C, then run restaurant.py with the same interpreter. The saved API order and reduced stock are still present. Press Enter at the product prompt to exit.

Existing databases may have different stock and order IDs, so compare changes rather than assuming a fresh database. Do not delete saved data merely to reproduce the demonstration.

## Explain the architecture

```text
Terminal (restaurant.py) or web requests (api.py)
                   |
                   v
Shared validation (ordering.py) and SQLite operations (database.py)
                   |
                   v
restaurant.db: products, stock and saved orders
                   |
                   v
Queue calculation (kitchen.py) -> simulated timings
```

## Troubleshooting

- Missing module: install requirements with the same Python interpreter used to start Uvicorn.
- requirements file missing: save exactly requirements.txt in the project folder; avoid requirements.txt.txt.
- PowerShell rejects -m: put `&` before a quoted executable path.
- Cannot import api: start from the folder containing api.py, or supply Uvicorn's --app-dir.
- Missing names imported from your files: update all changed source files, save them, and restart the server. GitHub updates do not automatically update a separate local copy.
- Page unreachable: confirm Uvicorn says Application startup complete and keep its process running.
- Editor warnings despite working imports: select the matching interpreter and reload the project in VS Code. Machine-specific editor paths should not be committed for other users.

## Tests on GitHub

The Python tests workflow runs on pushes, pull requests and manual dispatch, using Python 3.12 and 3.14. Open the Actions tab to see each run's result. A green run means the automated checks passed for those environments, not that every possible behaviour is proven. Database and API tests use temporary databases, preserving demonstration stock. The workflow follows GitHub's official Python testing guide: https://docs.github.com/en/actions/tutorials/build-and-test-code/python.
