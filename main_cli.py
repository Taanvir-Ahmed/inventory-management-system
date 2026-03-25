from pathlib import Path
from inventory import Inventory
from product import Product
from transactions import TransactionManager
from reports import ReportManager


DATA_FILE = Path(__file__).with_name("inventory_data.csv")


def print_menu() -> None:
    print(
        """
=============== Inventory Management System ===============
1. Display inventory
2. Add product
3. Update stock quantity
4. Restock product
5. Sell product
6. Update price
7. Search product by name
8. Show low-stock products
9. Save inventory to CSV
10. View transaction history
11. Show summary report
12. Show daily revenue report
0. Exit
===========================================================
"""
    )


def get_non_negative_int(prompt: str) -> int:
    while True:
        try:
            value = int(input(prompt))
            if value < 0:
                print("Please enter 0 or a positive whole number.")
                continue
            return value
        except ValueError:
            print("Invalid input. Please enter a whole number.")


def get_non_negative_float(prompt: str) -> float:
    while True:
        try:
            value = float(input(prompt))
            if value < 0:
                print("Please enter 0 or a positive number.")
                continue
            return value
        except ValueError:
            print("Invalid input. Please enter a valid number.")


def add_product_ui(inventory: Inventory) -> None:
    print("\n--- Add Product ---")
    product_id = input("Enter product ID: ").strip()
    name = input("Enter product name: ").strip()

    if not product_id or not name:
        print("Product ID and name cannot be empty.")
        return

    quantity = get_non_negative_int("Enter quantity: ")
    price = get_non_negative_float("Enter price (€): ")

    product = Product(product_id, name, quantity, price)
    if inventory.add_product(product):
        print(f"Product '{name}' added successfully.")
    else:
        print(f"A product with ID '{product_id}' already exists.")


def update_stock_ui(inventory: Inventory) -> None:
    print("\n--- Update Stock Quantity ---")
    product_id = input("Enter product ID: ").strip()
    new_quantity = get_non_negative_int("Enter new quantity: ")

    if inventory.update_stock(product_id, new_quantity):
        print("Stock quantity updated successfully.")
    else:
        print("Product not found or invalid quantity.")


def restock_ui(inventory: Inventory, transactions: TransactionManager) -> None:
    print("\n--- Restock Product ---")
    product_id = input("Enter product ID: ").strip()
    amount = get_non_negative_int("Enter quantity to add: ")

    product = inventory.find_by_id(product_id)
    if product is None:
        print("Product not found.")
        return

    if inventory.restock_product(product_id, amount):
        transactions.add_transaction("purchase", product.name, amount, product.price)
        print("Product restocked successfully.")
    else:
        print("Product not found.")


def sell_ui(inventory: Inventory, transactions: TransactionManager) -> None:
    print("\n--- Sell Product ---")
    product_id = input("Enter product ID: ").strip()
    amount = get_non_negative_int("Enter quantity to sell: ")

    product = inventory.find_by_id(product_id)
    if product is None:
        print("Product not found.")
    elif inventory.sell_product(product_id, amount):
        transactions.add_transaction("sale", product.name, amount, product.price)
        print("Sale completed successfully.")
    else:
        print(f"Not enough stock. Available quantity: {product.quantity}")


def update_price_ui(inventory: Inventory) -> None:
    print("\n--- Update Price ---")
    product_id = input("Enter product ID: ").strip()
    new_price = get_non_negative_float("Enter new price (€): ")

    if inventory.update_price(product_id, new_price):
        print("Price updated successfully.")
    else:
        print("Product not found.")


def search_product_ui(inventory: Inventory) -> None:
    print("\n--- Search Product ---")
    keyword = input("Enter product name or keyword: ").strip()
    matches = inventory.search_by_name(keyword)

    if not matches:
        print("No matching products found.")
        return

    print("\nMatches found:")
    for product in matches:
        print(
            f"{product.product_id} - {product.name} | "
            f"Qty: {product.quantity} | Price: €{product.price:.2f}"
        )


def show_low_stock_ui(inventory: Inventory) -> None:
    print("\n--- Low Stock Report ---")
    threshold = get_non_negative_int("Enter low-stock threshold: ")
    low_stock = inventory.low_stock_products(threshold)

    if not low_stock:
        print("All products are sufficiently stocked.")
        return

    for product in low_stock:
        print(f"{product.product_id} - {product.name}: {product.quantity} units")


def main() -> None:
    inventory = Inventory()
    inventory.load_from_csv(str(DATA_FILE))
    transactions = TransactionManager("transactions.json")
    reports = ReportManager(transactions)

    while True:
        print_menu()
        choice = input("Choose an option: ").strip()

        if choice == "1":
            inventory.display_inventory()
        elif choice == "2":
            add_product_ui(inventory)
        elif choice == "3":
            update_stock_ui(inventory)
        elif choice == "4":
            restock_ui(inventory, transactions)
        elif choice == "5":
            sell_ui(inventory, transactions)
        elif choice == "6":
            update_price_ui(inventory)
        elif choice == "7":
            search_product_ui(inventory)
        elif choice == "8":
            show_low_stock_ui(inventory)
        elif choice == "9":
            inventory.save_to_csv(str(DATA_FILE))
            print(f"Inventory saved to '{DATA_FILE.name}'.")
        elif choice == "10":
            transactions.show_transactions()
        elif choice == "11":
            reports.print_summary_report()
        elif choice == "12":
            reports.print_daily_revenue_report()
        elif choice == "0":
            inventory.save_to_csv(str(DATA_FILE))
            print("Inventory saved. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number from 0 to 12.")


if __name__ == "__main__":
    main()
