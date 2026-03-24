from dataclasses import dataclass


@dataclass
class Product:
    """Represents a single product in inventory."""
    product_id: str
    name: str
    quantity: int
    price: float

    def restock(self, amount: int) -> None:
        if amount < 0:
            raise ValueError("Restock amount cannot be negative.")
        self.quantity += amount

    def sell(self, amount: int) -> bool:
        if amount < 0:
            raise ValueError("Sale amount cannot be negative.")
        if amount > self.quantity:
            return False
        self.quantity -= amount
        return True

    def update_price(self, new_price: float) -> None:
        if new_price < 0:
            raise ValueError("Price cannot be negative.")
        self.price = new_price

    def to_csv_row(self) -> list[str]:
        return [self.product_id, self.name, str(self.quantity), f"{self.price:.2f}"]

    @property
    def total_value(self) -> float:
        return self.quantity * self.price
