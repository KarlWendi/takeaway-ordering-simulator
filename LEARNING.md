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
