import json
from datetime import datetime

class TransactionManager:
    def __init__(self, filename):
        self.filename = filename

    def load_transactions(self):
        try:
            with open(self.filename, "r") as file:
                return json.load(file)
        except:
            return []

    def save_transactions(self, transactions):
        with open(self.filename, "w") as file:
            json.dump(transactions, file, indent=4)

    def add_transaction(self, t_type, product, quantity, price):
        transactions = self.load_transactions()

        transaction = {
            "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "type": t_type,
            "product": product,
            "quantity": quantity,
            "total": round(quantity * price, 2)
        }

        transactions.append(transaction)
        self.save_transactions(transactions)

    def show_transactions(self):
        transactions = self.load_transactions()

        if not transactions:
            print("No transactions found.")
            return

        print("\nTransaction History:")
        for t in transactions:
            print(t)