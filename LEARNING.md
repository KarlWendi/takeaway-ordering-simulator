# Learning log

## Stage 1 — represent and display a menu

### Business purpose

An ordering system needs a consistent catalogue of products and prices. Start with that catalogue before accepting orders.

### Read menu.py from top to bottom

1. The opening triple-quoted string is a docstring: an explanation of the file.
2. `MENU` is a variable holding a list. Square brackets contain a sequence of items. The capitalised name indicates a value we intend to treat as a constant; Python does not enforce that.
3. Each item is a dictionary, written with curly braces. A dictionary maps keys such as `name` to values such as `Burger`.
4. An `id` identifies a product independently of its name or position. A list position starts at zero; our product IDs start at one. They are different concepts.
5. Prices are integers in pence. 399 means £3.99. This keeps later calculations exact rather than using floating-point money.
6. `def format_price(pence):` defines a reusable function. `pence` is its parameter. When called with `399`, that value becomes the parameter's value for the call.
7. `divmod(399, 100)` produces the quotient 3 and remainder 99. Assignment stores those two results in two variables.
8. The f-string inserts values into text. `:02d` formats the remainder as a two-digit integer, so 5 pence becomes `05`.
9. `return` sends a result back to the caller. It does not print it.
10. `display_menu()` loops through the list using `for`. On each iteration, `item` refers to one dictionary.
11. `item["price_pence"]` retrieves the value associated with that key. It is a dictionary lookup, not a list position.
12. `print` writes text to the terminal. Python uses indentation to group statements inside functions and loops.
13. The `if __name__ == "__main__":` guard runs the display only when this file is executed directly. Importing the file later lets us reuse its functions without printing the menu automatically.

### Trace one product

For Burger, the dictionary provides 399. `format_price(399)` returns `£3.99`. The display function inserts that text alongside product ID 1 and the name Burger, then prints the completed line.

### Verification

The script displayed the expected menu. Formatting checks: 0 → £0.00, 5 → £0.05, 100 → £1.00, 399 → £3.99.

### Try before stage 2

- Predict what `format_price(105)` returns, then run it to check.
- Add a fictional drink with ID 4 and a price of 150 pence. Predict the extra output line.
- Explain why returning a price is different from printing it.
- Explain why a product ID is different from its list position.

### GitHub concepts

A repository holds project files and their history. A commit records a snapshot with a message explaining the change. A push uploads local commits to GitHub; creating or uploading files in GitHub's website can also create a commit. The stage-1 commit should say `Stage 1: add fictional menu and learning guide`. Later stages should add real changes rather than pretending all planned features already exist.

## Stage 2 — choose a product and calculate an order

### Business purpose

Customers must choose an existing product and a sensible quantity. Validate those choices before calculating a price. This stage provides a quote; it does not accept payment, check stock or persist an order.

### Read ordering.py

1. `from menu import ...` reuses stage-1 data and functions. The main guard in menu.py prevents an automatic display during import.
2. `find_item(item_id)` performs a linear search: examine each product until its ID matches. `==` compares values; `=` assigns a value. A successful `return` ends the function immediately.
3. Product IDs are identifiers, not list positions. ID 42 can identify the first element in a list.
4. If the loop ends without a match, `raise ValueError(...)` signals a failure instead of returning a made-up product.
5. `calculate_order` validates both parameters before using them. `type(quantity) is not int` requires an actual integer, rejecting strings, fractions and booleans. Booleans are deliberately rejected because Python otherwise treats them as a kind of integer.
6. `1 <= quantity <= 50` checks both boundaries. `not` reverses the result; `or` means either invalid condition is enough to reject the value. Fifty is an invented project rule, not a restaurant policy.
7. `price_pence * quantity` calculates the total. Two burgers: 399 × 2 = 798 pence = £7.98.
8. The returned dictionary contains the result, allowing a future API or database component to reuse the function. Calculation does not print, change MENU or save data.
9. `input` always returns text. `int("2")` converts it to an integer; `int("hello")` raises ValueError. We catch conversion errors separately to give a helpful message.
10. `try` runs code that may fail. `except ValueError as error` catches that specific failure and stores its explanation. Unexpected kinds of failures are not silently hidden.
11. `main()` handles terminal interaction and display. Separating it from calculation lets tests call the business logic without typing into the terminal.

### Trace a successful order

User types `1` and `2` → convert both strings to integers → validate → find Burger by ID → calculate 399 × 2 → return an order dictionary → format 798 as £7.98 → print the summary.

### Trace a rejected order

User types `1` and `0` → conversion succeeds → quantity validation fails → raise ValueError → main catches it → print the rejection. No summary is produced.

### Verification and tests

`test_ordering.py` uses Python's built-in unittest module. An assertion compares the actual result with an expected result. A rejection test expects ValueError. Tests cover different prices, valid quantity boundaries, invalid inputs and an ID unrelated to list position. `patch` temporarily substitutes a tiny fictional menu to check the last case, then restores it. Six test methods passed. Terminal checks also covered successful input, an unknown ID, zero quantity and non-numeric input.

### Try before stage 3

- Predict the total for product 2 with quantity 3.
- Explain why `input("Quantity: ")` returns text even if you type a number.
- Explain the difference between returning an order dictionary and saving it in a database.
- Predict what happens for product ID 999, quantity 1.

### Main takeaway

Turn user input into validated data before doing business calculations. Keep calculation separate from display so the same logic can later serve a terminal, API or tests.

### GitHub milestone

Commit: `Stage 2: add validated order calculation and tests`. View its changes to see new ordering and test files, an updated roadmap and this explanation. Stage 1 remains accessible in commit history.

## Stage 3 — save orders and track stock with SQLite

### Files to create in your editor

Keep menu.py and ordering.py. Add database.py, restaurant.py and test_database.py in the same folder. Update ordering.py with the small shared-validation refactor in the Stage 3 commit. Run `python restaurant.py`. SQLite is included in Python: do not install a package called sqlite3. restaurant.db appears automatically; it is a data file, not Python code to paste into an editor.

### Business purpose

Stage 2 calculated a quote and forgot it when the program ended. Stage 3 saves the order and reserves finished-product stock. It must reject unavailable products and must never deduct stock without saving the corresponding order.

### Database vocabulary

- SQLite is the database management system. sqlite3 is Python's interface to it.
- A database file stores data on disk; ours is restaurant.db.
- A table is a collection of records with named columns. A row represents one product or order.
- A primary key uniquely identifies a row. SQLite generates integer order IDs when we omit them during insertion.
- A foreign key links orders.item_id to products.id. PRAGMA foreign_keys enables enforcement on each connection.
- SQL is the language we use to query and change the database.
- A connection is the program's access to the database; close it when finished.
- A transaction groups changes into one unit. Commit keeps successful changes; rollback undoes changes when an error escapes the transaction block.

### Our tables

products: id, name, price_pence, stock.

orders: id, item_id, quantity, total_pence, status, created_at.

The total is saved at the time of ordering. Later price changes should not alter what an earlier order cost. The displayed name is currently joined from products, so a later product rename would change the name shown for older orders. Status defaults to queued and the timestamp uses SQLite's UTC current time.

### Read database.py in sections

1. Imports: sqlite3 opens the database; Path constructs a file path. We reuse MENU and extract validate_order_input from Stage 2 so both quote and database stages use the same rules.
2. DATABASE_PATH resolves restaurant.db beside database.py. Running from another terminal folder will still use the same database.
3. connect(): open the file, configure named-column row access and enforce foreign keys. sqlite3.Row allows `row["stock"]`; dict(row) converts the result to ordinary data for the rest of the program.
4. initialise_database(): CREATE TABLE IF NOT EXISTS creates each table on first run. NOT NULL requires a value; CHECK rejects invalid stored values. ON CONFLICT(id) DO NOTHING avoids overwriting a product that already exists. This preserves stock on restart. New products missing from INITIAL_STOCK start at zero stock.
5. get_menu(): SELECT reads records. ORDER BY id puts them in a predictable order. fetchall() retrieves all result rows.
6. place_order(): validate parameters, then UPDATE a matching product only if stock is sufficient. SET stock = stock - ? deducts the requested amount. rowcount tells us whether a product row was updated. Zero updated rows means either no such product or insufficient stock; a SELECT distinguishes the two.
7. The SQL placeholders `?` receive values separately in a tuple. This avoids building SQL instructions from user input. `(item_id,)` is a one-element tuple; the comma matters.
8. After reserving stock, read the product's price and INSERT an order. lastrowid gives the newly generated order ID.
9. `with connection:` commits when the block succeeds or rolls back when an exception leaves it. It does not close the connection. `finally` closes the connection whether the operation succeeded or failed. We return success after the transaction has committed.
10. get_orders(): JOIN links orders to products using their shared product ID so we can display the product name alongside each saved order.

### Read restaurant.py

This is the terminal interface. It initialises the database, shows stock and saved orders, converts typed input and calls place_order. Pressing Enter at the product prompt exits. Earlier stages remain independently runnable. This separation means a later API can call database functions without depending on terminal input or output.

### Trace two burgers

Start: burger stock 20, no orders → validate ID 1 and quantity 2 → reserve two burgers → stock becomes 18 inside the transaction → read price 399 → insert order total 798 → commit → display order ID and £7.98. Close and restart Python: stock is still 18 and the order still exists.

### Why a transaction matters

Suppose stock decreases successfully but inserting the order fails. Without a transaction, those two units could disappear from available stock with no order explaining why. With our transaction, the failed insert triggers rollback, restoring stock. A test deliberately forces that failure to verify the behaviour. The conditional stock UPDATE also makes availability checking and reservation a single database operation.

### Verification

Seven database tests use fresh temporary databases so they do not change your demonstration stock. They cover saved totals and stock, preservation on reinitialisation, unknown IDs, invalid quantities, insufficient stock, ordering the last units and rollback after a forced insert failure. Together with Stage 2, all 13 tests passed. A separate-process check placed two burgers, reopened the same database in another Python process and verified stock 18 and one saved order.

### Try it yourself

1. Run restaurant.py and order product 1, quantity 2. On a fresh database you get order #1 and £7.98.
2. Run it again: stock is 18 and the saved order is listed. Press Enter to exit.
3. Run again and request 19 burgers: it should reject the order because only 18 remain.
4. Run again: stock and order count should be unchanged by that rejection.
5. Explain what would go wrong if we reset stock to 20 every startup.

### Main takeaway

Use a database for information that must survive a restart, and use a transaction when several changes must succeed together. A saved order and its stock deduction represent one business action.

### GitHub milestone

Commit: `Stage 3: persist orders and stock with SQLite`. Commit the Python source, tests and explanations. Ignore restaurant.db: it is generated local data and each reader can create their own fresh database by running the program.

## Stage 4 — expose the system through a mock API

### Files for your editor

Add api.py, requirements.txt and test_api.py. Update database.py to the latest version; it now defines ItemNotFoundError and InsufficientStockError. Keep menu.py, ordering.py and restaurant.py. All Python files belong in the same folder. You do not need to replace restaurant.db.

Install with `python -m pip install -r requirements.txt` and start with `python -m uvicorn api:app --reload`. Run from your project folder, not VS Code's installation folder. Open http://127.0.0.1:8000/docs. VS Code's Run Python File button does not start this API server by itself. See README.md for full instructions.

### Business purpose and vocabulary

An API (application programming interface) provides an agreed way for another program to request operations. Our mock API simulates a takeaway backend using fictional data. A future kiosk or website could call it; this stage does not build that customer website.

- Client: the program sending a request; the documentation page can act as a testing client.
- Server: the running program receiving requests. Uvicorn runs our FastAPI application.
- HTTP: the protocol used for these web requests and responses.
- Endpoint: an operation identified by method and path, such as POST /orders. GET /orders is a different operation on the same path.
- JSON: text encoding structured data. The request body `{"item_id": 1, "quantity": 2}` carries the order input.
- Response: the result sent back, including a status code and usually a JSON body.
- Localhost: 127.0.0.1 means your own computer. 8000 is the port Uvicorn listens on by default. The server must remain running for the address to work.

### Read api.py in sections

1. Imports load FastAPI, its HTTPException type, Pydantic validation tools and our existing database operations.
2. OrderRequest is a class describing the required request fields. It inherits BaseModel, so Pydantic can parse and validate incoming data. `item_id: int` is a type annotation, describing the intended type. Here the validation library enforces it.
3. Field(strict=True, gt=0) requires a real integer greater than zero. Quantity must be 1–50. Strict mode rejects "2", true and fractions rather than silently converting them. ConfigDict(extra="forbid") rejects unexpected fields.
4. create_app(database_path) builds an application using a chosen database. The normal app uses restaurant.db; tests supply a temporary path so they do not consume your stock. The nested functions remember the path supplied when the application was created.
5. lifespan initialises the database once when the server starts. `yield` separates startup from shutdown. asynccontextmanager is the framework-supported context-manager pattern; ordinary database endpoints remain normal `def` functions. You do not need to rewrite all your code as asynchronous code.
6. FastAPI(...) creates the application and gives the documentation a title and version.
7. A decorator such as `@application.get("/menu")` registers the function below it as the handler for that endpoint. FastAPI calls it when a matching request arrives. Its returned Python list/dictionary is converted into a JSON response.
8. POST /orders receives an OrderRequest. It calls place_order with its validated values. The normal response code is 201, meaning a record was created.
9. The database's specific error types are subclasses of ValueError. Existing terminal code still catches them, while the API can distinguish product missing (404) from insufficient stock (409) without comparing message text. HTTPException sends the appropriate error response. `from error` preserves the original exception as the cause for debugging.
10. `app = create_app()` makes the application Uvicorn loads. `api:app` in the start command means module api.py, object app. `--reload` restarts the development server when code files change. Importing or running api.py by itself does not start Uvicorn.

### Trace a web order

Client submits POST /orders with JSON → FastAPI validates OrderRequest → handler calls place_order → SQLite reserves stock and saves order in one transaction → handler returns order dictionary → FastAPI sends JSON with status 201. Invalid request fields return 422 before database changes. A valid request for a missing product returns 404. A valid request exceeding current stock returns 409.

### Test through the documentation page

1. Start the server and open /docs.
2. GET /menu → Try it out → Execute. Note burger stock.
3. POST /orders → Try it out → submit item_id 1, quantity 2 → Execute.
4. Read the response: code 201, order_id and total_pence 798.
5. GET /menu again: stock is two lower. GET /orders: the new order appears.
6. Submit quantity 0: code 422 and no saved order.
7. Submit item_id 999, quantity 1: code 404 and no saved order.
8. Stop with Ctrl+C. Run restaurant.py: the API-created order appears because both interfaces use the same local database.

Every successful POST creates a new order. Repeating Execute is another purchase simulation; the code does not yet recognise duplicate submissions. GET requests only read data.

### Verification

Eight API tests use TestClient, which simulates HTTP requests without a separate network server. Its context manager runs startup so each temporary database is initialised. Tests verify responses and actual database effects, including rejected requests leaving stock and orders unchanged. All 21 project tests passed. /docs and its OpenAPI schema are also checked.

### Main takeaway

The same business logic can serve different interfaces. The terminal accepts typed input; the API accepts web requests. Both use the same validated database operations, so stock and order rules stay consistent.

### GitHub milestone and limits

Commit: `Stage 4: add mock ordering API and HTTP tests`. The repository contains runnable code, install instructions and this guide. Uploading Python to GitHub does not run a server. This stage is a local demo without authentication, payments, a customer website or production deployment.

### Official references

- Request bodies: https://fastapi.tiangolo.com/tutorial/body/
- API testing: https://fastapi.tiangolo.com/tutorial/testing/
- Application startup: https://fastapi.tiangolo.com/advanced/events/

## Stage 5 — simulate kitchen queue timing

### Files and running

Add kitchen.py and queue_demo.py beside your existing Python files. Update api.py for GET /queue. The new test_kitchen.py and updated test_api.py record verification. No database schema or requirements changes are needed. `python queue_demo.py` runs a fictional comparison without reading or changing your saved orders. GET /queue in the API documentation simulates your actual saved queued orders without modifying them.

### Business question

How does kitchen capacity affect waiting time? A station means one independent preparation slot in this simplified model. This is an educational model, not measured restaurant performance.

### Algorithm steps

1. Validate that station count is a whole number from 1 to 10.
2. Start every station's available time at zero.
3. Consider orders in increasing ID order, skipping orders whose status is not queued.
4. Calculate preparation duration: configured minutes per unit multiplied by quantity.
5. Find the station available soonest.
6. Start there when it is free; finish equals start plus preparation duration.
7. Update that station's available time and record the result.
8. Summarise average wait, longest wait and time until all orders are ready.

This is a greedy scheduling rule: choose the earliest-free station for each next order. It does not guarantee the best possible ordering of jobs. We preserve ID order as an approximation of arrival order.

### Trace the two-station example

Orders: two burgers take 6 minutes; one fries takes 2; one wrap takes 4.

Initially available_at = [0, 0]. Both stations are free. Order 1 uses station 1 (the first station wins a tie), starts at zero and finishes at six: [6, 0]. Order 2 uses station 2, starts at zero and finishes at two: [6, 2]. Order 3 uses station 2 because two is earlier than six. It starts at two and finishes at six: [6, 6].

Waiting times are [0, 0, 2], so average wait = (0 + 0 + 2) / 3 = 0.67 minutes, rounded. Every order is ready by minute six.

### Read kitchen.py

- PREP_MINUTES maps product IDs to invented per-unit preparation durations. This configuration is separate from money and stock.
- `[0] * stations` constructs a list with one zero per station. Each entry stores when that station next becomes available.
- `sorted(..., key=lambda order: order["id"])` makes an ID-ordered list without reordering the input. A lambda is a short anonymous function that tells sorted which value to compare.
- `continue` skips the remainder of the loop for a non-queued order.
- `min(range(stations), key=lambda index: available_at[index])` returns the index of the earliest-free station. Indices start at zero; display station numbers use index + 1.
- Each output dictionary records preparation duration, waiting time and ready time. Waiting is the simulated start time because all orders begin waiting at minute zero.
- `sum` adds waiting times. Divide by order count for the mean. Empty queues return zero, avoiding division by zero.
- `max(available_at)` gives when the last busy station finishes. Extra free stations have zero and do not extend that time.
- The simulator returns data rather than printing it or saving changes. queue_demo.py prints the fictional example, and api.py returns the same kind of data as JSON.

### Waiting versus completion

For order 3 in the two-station example, waiting is 2 minutes and preparation is 4, giving completion after 6 minutes. A third station lets it start immediately and finish after 4, but order 1 still takes 6. Adding capacity can reduce waiting without reducing when every order is done.

| Stations | Average waiting minutes | All orders ready after minutes |
| --- | --- | --- |
| 1 | 4.67 | 12 |
| 2 | 0.67 | 6 |
| 3 | 0 | 6 |

These findings apply to this fixed example under the stated assumptions, not every workload or a real restaurant.

### Query parameters

GET /queue?stations=2 uses a URL query parameter rather than a JSON body. FastAPI's Query sets the default to 2 and allowed bounds to 1–10. In /docs, change the stations field and Execute. This operation reads queued orders and computes a schedule; repeating it does not place new orders.

### Assumptions and limits

Simulation time starts at zero on every call. We ignore historical created_at times and assume all currently queued orders are available at zero, with all stations free. There is no live countdown or completed-order update. Stations are identical and can prepare every product; each handles one whole order at a time. Preparation duration is proportional to quantity, with no batching or equipment restrictions. Adding products requires configuring their times; missing configuration raises a clear error. Stock reservation happened when ordering and is not repeated by queue calculation.

### Efficiency

For n orders and s stations, sorting costs O(n log n) and finding a station for each order costs O(n × s). Our small model allows at most ten stations, so a simple scan is easy to read. Larger systems could use a priority queue for station availability. Output and sorted order lists use O(n) space; station availability uses O(s).

### Verification and GitHub

Eight scheduling tests cover exact two-station assignment, one and three stations, empty queues, filtering and ID order, invalid station counts, missing preparation times and unchanged inputs. Two API tests check query validation and that simulation leaves stock and saved orders unchanged. All 31 project tests passed, and queue_demo.py produced the table above.

Commit: `Stage 5: simulate kitchen queues and compare capacity`. The example, comparison and assumptions make the algorithm reviewable.

### Main takeaway and exercises

A scheduling algorithm turns assumptions about work and capacity into predicted timings. Compare scenarios and explain both the result and the model's limits.

1. Predict the start and finish times for the third order with one station.
2. Explain why three stations do not finish every order sooner than two in our example.
3. Change DEMO_ORDERS quantities and predict which station gets the next order.
4. Explain why repeatedly reading GET /queue does not reduce stock or mark orders completed.

## Stage 6 — make the project demonstrable and explainable

### Deliverables

DEMO.md lets another person install and demonstrate the project. RESULTS.md records a reproducible workload and the observed saved-order snapshot, separating the two and spelling out assumptions. INTERVIEW.md provides explanation prompts and exercises. The README links them and displays test status.

### Automatic checks on GitHub

.github/workflows/tests.yml is a YAML configuration file, not Python code. It tells GitHub Actions when and how to run checks. A push uploads a commit; a pull request proposes changes for review; workflow_dispatch allows a manual run. Our workflow runs on all three triggers.

A job runs on a fresh GitHub-hosted Ubuntu computer. checkout retrieves the repository; setup-python selects Python. The version matrix runs the same job on Python 3.12 and 3.14. Pip installs the requirements; unittest discovers and runs test_*.py files; queue_demo.py checks the demonstration. Read-only contents permission is enough. Nothing deploys a site or changes your local database.

A green check means those commands passed in the recorded environments. A red check means open the run log and find the failing step. Tests reduce uncertainty but do not prove absence of every bug. Changes made only in a local editor do not reach GitHub or trigger this workflow until committed and pushed.

### Completion and understanding

The original implementation requirements are now represented by the mock API, SQLite inventory/orders and a queue algorithm. The portfolio contains the runnable source, development history, tests, demonstration and limitations. Your learning continues through practising explanations and making changes yourself. Use INTERVIEW.md to check your understanding, and acknowledge AI assistance accurately.

## Stage 7: Python website

Streamlit generates a page from Python widgets. website.py calls web_client.py, which sends HTTP requests to FastAPI. The API still validates input and updates SQLite in a transaction. WEBSITE.md explains setup and each step.

Streamlit reruns scripts after interactions. Only a submitted form sends POST. Refresh and station changes send GET and cannot deduct stock. Session state carries the confirmation through a rerun. Network failures are never automatically retried: the server may have saved the order before the connection failed.

Trace the order button to the database transaction, then explain why the slider cannot place orders. Three interface tests use a temporary API database to check successful submission, refresh safety, insufficient stock and unavailable-service help.

## Stage 8: public hosting

A hosting provider runs Python on its servers, so a visitor needs only the website address. Streamlit and FastAPI are separate services. TAKEAWAY_API_URL connects them; localhost would point to the hosting server itself. The chosen free demo has shared fictional stock and temporary orders that reset on restarts. Local saved data is never uploaded.

Render deploys from GitHub commits. GitHub Actions verifies tests; hosting builds and starts the servers. GET calls allow time for free services to wake up, while POST is never automatically retried. DEPLOYMENT.md explains the setup.

## Expanded menu

The catalogue now has 12 products. Each new ID has a price in menu.py, initial stock in database.py and an invented preparation time in kitchen.py. New rows are seeded on API startup without overwriting existing local stock or orders. The website uses rows of three cards so a larger menu remains readable. Free public redeployments reset demo data as described above.
