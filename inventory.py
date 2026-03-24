import csv
from pathlib import Path
from product import Product


class Inventory:
    """Stores and manages all products."""

    def __init__(self) -> None:
        self.products: dict[str, Product] = {}

    def add_product(self, product: Product) -> bool:
        if product.product_id in self.products:
            return False
        self.products[product.product_id] = product
        return True

    def find_by_id(self, product_id: str) -> Product | None:
        return self.products.get(product_id)

    def search_by_name(self, keyword: str) -> list[Product]:
        keyword = keyword.lower().strip()
        return [
            product
            for product in self.products.values()
            if keyword in product.name.lower()
        ]

    def update_stock(self, product_id: str, new_quantity: int) -> bool:
        product = self.find_by_id(product_id)
        if product is None or new_quantity < 0:
            return False
        product.quantity = new_quantity
        return True

    def restock_product(self, product_id: str, amount: int) -> bool:
        product = self.find_by_id(product_id)
        if product is None:
            return False
        product.restock(amount)
        return True

    def sell_product(self, product_id: str, amount: int) -> bool:
        product = self.find_by_id(product_id)
        if product is None:
            return False
        return product.sell(amount)

    def update_price(self, product_id: str, new_price: float) -> bool:
        product = self.find_by_id(product_id)
        if product is None:
            return False
        product.update_price(new_price)
        return True

    def low_stock_products(self, threshold: int = 20) -> list[Product]:
        return [product for product in self.products.values() if product.quantity < threshold]

    def total_inventory_value(self) -> float:
        return sum(product.total_value for product in self.products.values())

    def display_inventory(self) -> None:
        if not self.products:
            print("\nInventory is empty.")
            return

        print("\n" + "=" * 78)
        print(f"{'ID':<8}{'Product':<22}{'Quantity':<12}{'Price (€)':<15}{'Value (€)':<15}")
        print("-" * 78)

        for product in sorted(self.products.values(), key=lambda item: item.name.lower()):
            print(
                f"{product.product_id:<8}{product.name:<22}{product.quantity:<12}"
                f"{product.price:<15.2f}{product.total_value:<15.2f}"
            )

        print("-" * 78)
        print(f"{'Total inventory value':<57}{self.total_inventory_value():<15.2f}")
        print("=" * 78)

    def load_from_csv(self, file_name: str) -> None:
        path = Path(file_name)
        self.products.clear()

        try:
            with open(path, "r", newline="", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                for line_number, row in enumerate(reader, start=2):
                    product_id = row["product_id"].strip()
                    name = row["name"].strip()
                    quantity = int(row["quantity"])
                    price = float(row["price"])

                    if quantity < 0 or price < 0:
                        raise ValueError(
                            f"Negative value found in CSV on line {line_number}."
                        )

                    product = Product(product_id, name, quantity, price)
                    if not self.add_product(product):
                        raise ValueError(
                            f"Duplicate product_id '{product_id}' found on line {line_number}."
                        )
        except FileNotFoundError:
            print(f"CSV file '{file_name}' not found. Starting with empty inventory.")
        except (KeyError, ValueError) as error:
            print(f"Error while loading CSV: {error}")
            self.products.clear()

    def save_to_csv(self, file_name: str) -> None:
        path = Path(file_name)
        with open(path, "w", newline="", encoding="utf-8") as file:
            fieldnames = ["product_id", "name", "quantity", "price"]
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()

            for product in sorted(self.products.values(), key=lambda item: item.product_id):
                writer.writerow(
                    {
                        "product_id": product.product_id,
                        "name": product.name,
                        "quantity": product.quantity,
                        "price": f"{product.price:.2f}",
                    }
                )
