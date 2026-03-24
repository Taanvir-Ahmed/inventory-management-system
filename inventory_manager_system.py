from pathlib import Path


def read_inventory(file_name: str) -> dict:
    """Read inventory data from a text file into a nested dictionary."""
    inventory = {}

    try:
        with open(file_name, "r", encoding="utf-8") as file:
            for line_number, line in enumerate(file, start=1):
                line = line.strip()

                if not line:
                    continue

                parts = [part.strip() for part in line.split(":")]
                if len(parts) != 3:
                    raise ValueError(
                        f"Invalid format on line {line_number}: '{line}'. "
                        "Expected format: Product: quantity: price"
                    )

                product, quantity_text, price_text = parts

                if product in inventory:
                    raise ValueError(f"Duplicate product found on line {line_number}: {product}")

                quantity = int(quantity_text)
                price = float(price_text)

                if quantity < 0 or price < 0:
                    raise ValueError(
                        f"Negative quantity or price found on line {line_number}: '{line}'"
                    )

                inventory[product] = {"quantity": quantity, "price": price}

        return inventory

    except FileNotFoundError:
        print(f"Error: file '{file_name}' was not found.")
        return {}
    except ValueError as error:
        print(f"Error while reading inventory: {error}")
        return {}


def display_inventory(inventory: dict) -> None:
    """Print inventory in a formatted table."""
    if not inventory:
        print("\nInventory is empty.")
        return

    print("\n" + "=" * 68)
    print(f"{'Product':<20}{'Quantity':<15}{'Price (€)':<15}{'Value (€)':<15}")
    print("-" * 68)

    total_value = 0.0
    for product in sorted(inventory):
        quantity = inventory[product]["quantity"]
        price = inventory[product]["price"]
        value = quantity * price
        total_value += value
        print(f"{product:<20}{quantity:<15}{price:<15.2f}{value:<15.2f}")

    print("-" * 68)
    print(f"{'Total inventory value':<50}{total_value:<15.2f}")
    print("=" * 68)


def add_product(inventory: dict) -> None:
    """Add a new product to inventory."""
    print("\n--- Add Product ---")
    product = input("Enter product name: ").strip()

    if not product:
        print("Product name cannot be empty.")
        return

    if product in inventory:
        print(f"'{product}' already exists. Use update stock instead.")
        return

    try:
        quantity = int(input("Enter quantity: "))
        price = float(input("Enter price (€): "))

        if quantity < 0 or price < 0:
            print("Quantity and price must be zero or greater.")
            return

        inventory[product] = {"quantity": quantity, "price": price}
        print(f"Product '{product}' added successfully.")
    except ValueError:
        print("Invalid input. Quantity must be an integer and price must be a number.")


def update_stock(inventory: dict) -> None:
    """Update quantity for an existing product."""
    print("\n--- Update Stock ---")
    product = input("Enter product name to update: ").strip()

    if product not in inventory:
        print(f"'{product}' not found in inventory.")
        return

    try:
        new_quantity = int(input(f"Enter new quantity for {product}: "))
        if new_quantity < 0:
            print("Quantity cannot be negative.")
            return

        inventory[product]["quantity"] = new_quantity
        print(f"Stock updated: {product} now has {new_quantity} units.")
    except ValueError:
        print("Invalid quantity. Please enter a whole number.")


def update_price(inventory: dict) -> None:
    """Update price for an existing product."""
    print("\n--- Update Price ---")
    product = input("Enter product name to update price: ").strip()

    if product not in inventory:
        print(f"'{product}' not found in inventory.")
        return

    try:
        new_price = float(input(f"Enter new price for {product} (€): "))
        if new_price < 0:
            print("Price cannot be negative.")
            return

        inventory[product]["price"] = new_price
        print(f"Price updated: {product} now costs €{new_price:.2f}.")
    except ValueError:
        print("Invalid price. Please enter a valid number.")


def get_low_stock(inventory: dict, threshold: int = 20) -> list:
    """Return a list of low-stock products."""
    return [product for product, data in inventory.items() if data["quantity"] < threshold]


def show_low_stock(inventory: dict) -> None:
    """Display low-stock products."""
    print("\n--- Low Stock Report ---")
    low_stock_items = get_low_stock(inventory)

    if not low_stock_items:
        print("All products are sufficiently stocked.")
        return

    for product in sorted(low_stock_items):
        print(f"{product}: {inventory[product]['quantity']} units remaining")


def search_product(inventory: dict) -> None:
    """Search for a product by name."""
    print("\n--- Search Product ---")
    keyword = input("Enter product name or keyword: ").strip().lower()

    matches = [product for product in inventory if keyword in product.lower()]

    if not matches:
        print("No matching products found.")
        return

    for product in sorted(matches):
        quantity = inventory[product]["quantity"]
        price = inventory[product]["price"]
        print(f"{product} -> Quantity: {quantity}, Price: €{price:.2f}")


def save_inventory(inventory: dict, file_name: str) -> None:
    """Save inventory to text file."""
    try:
        with open(file_name, "w", encoding="utf-8") as file:
            for product in sorted(inventory):
                quantity = inventory[product]["quantity"]
                price = inventory[product]["price"]
                file.write(f"{product}: {quantity}: {price:.2f}\n")
        print(f"Inventory saved successfully to '{file_name}'.")
    except OSError as error:
        print(f"Error saving file: {error}")


def print_menu() -> None:
    """Display the main menu."""
    print(
        """
========== Inventory Management System ==========
1. Display inventory
2. Add product
3. Update stock
4. Update price
5. Search product
6. Show low-stock products
7. Save inventory
0. Exit
=================================================
"""
    )


def main() -> None:
    """Run the inventory management system."""
    file_name = Path(__file__).with_name("inventory_big.txt")
    inventory = read_inventory(str(file_name))

    if not inventory:
        print("Program started with an empty inventory.")

    while True:
        print_menu()
        choice = input("Choose an option: ").strip()

        if choice == "1":
            display_inventory(inventory)
        elif choice == "2":
            add_product(inventory)
        elif choice == "3":
            update_stock(inventory)
        elif choice == "4":
            update_price(inventory)
        elif choice == "5":
            search_product(inventory)
        elif choice == "6":
            show_low_stock(inventory)
        elif choice == "7":
            save_inventory(inventory, str(file_name))
        elif choice == "0":
            save_inventory(inventory, str(file_name))
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please select a number from the menu.")


if __name__ == "__main__":
    main()
