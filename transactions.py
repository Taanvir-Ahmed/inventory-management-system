import json
from datetime import datetime
from pathlib import Path


class TransactionManager:
    def __init__(self, file_name: str) -> None:
        self.file_path = Path(__file__).with_name(file_name)

    def load_transactions(self) -> list:
        try:
            with open(self.file_path, "r", encoding="utf-8") as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def save_transactions(self, transactions: list) -> None:
        with open(self.file_path, "w", encoding="utf-8") as file:
            json.dump(transactions, file, indent=4)

    def add_transaction(
        self, transaction_type: str, product_name: str, quantity: int, price: float
    ) -> None:
        transactions = self.load_transactions()
        transaction = {
            "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "type": transaction_type,
            "product": product_name,
            "quantity": quantity,
            "price": round(price, 2),
            "total": round(quantity * price, 2),
        }
        transactions.append(transaction)
        self.save_transactions(transactions)

    def show_transactions(self) -> None:
        transactions = self.load_transactions()
        if not transactions:
            print("\nNo transactions found.")
            return

        print("\n" + "=" * 86)
        print(f"{'Date':<18}{'Type':<12}{'Product':<22}{'Qty':<8}{'Price (€)':<12}{'Total (€)':<12}")
        print("=" * 86)
        for t in transactions:
            print(
                f"{t['date']:<18}{t['type'].upper():<12}{t['product']:<22}"
                f"{t['quantity']:<8}{t['price']:<12.2f}{t['total']:<12.2f}"
            )
        print("=" * 86)
