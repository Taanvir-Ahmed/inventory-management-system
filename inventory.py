import csv
from pathlib import Path
from product import Product


class Inventory:
    def __init__(self) -> None:
        self.products: dict[str, Product] = {}

    def add_product(self, product: Product) -> bool:
        if product.product_id in self.products:
            return False
        self.products[product.product_id] = product
        return True

    def find_by_id(self, product_id: str):
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
        if product is None or amount < 0:
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
        if product is None or new_price < 0:
            return False
        product.price = new_price
        return True

    def low_stock_products(self, threshold: int) -> list[Product]:
        return [
            product for product in self.products.values() if product.quantity <= threshold
        ]

    def display_inventory(self) -> None:
        if not self.products:
            print("\nNo products in inventory.")
            return

        print("\n" + "=" * 70)
        print(f"{'ID':<8}{'Name':<22}{'Quantity':<12}{'Price (€)':<12}{'Value (€)':<12}")
        print("=" * 70)
        for product in self.products.values():
            value = product.quantity * product.price
            print(
                f"{product.product_id:<8}{product.name:<22}{product.quantity:<12}"
                f"{product.price:<12.2f}{value:<12.2f}"
            )
        print("=" * 70)

    def load_from_csv(self, file_name: str) -> None:
        file_path = Path(file_name)
        if not file_path.exists():
            return

        with open(file_path, "r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                try:
                    product = Product(
                        row["product_id"].strip(),
                        row["name"].strip(),
                        int(row["quantity"]),
                        float(row["price"]),
                    )
                    self.products[product.product_id] = product
                except (KeyError, ValueError, TypeError):
                    continue

    def save_to_csv(self, file_name: str) -> None:
        with open(file_name, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["product_id", "name", "quantity", "price"])
            for product in self.products.values():
                writer.writerow(
                    [product.product_id, product.name, product.quantity, product.price]
                )
