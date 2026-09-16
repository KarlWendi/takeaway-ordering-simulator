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
