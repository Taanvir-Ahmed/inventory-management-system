from pathlib import Path
import tkinter as tk

from gui import InventoryApp
from inventory import Inventory
from reports import ReportManager
from transactions import TransactionManager


DATA_FILE = Path(__file__).with_name("inventory_data.csv")


def main() -> None:
    inventory = Inventory()
    inventory.load_from_csv(str(DATA_FILE))

    transactions = TransactionManager("transactions.json")
    reports = ReportManager(transactions)

    root = tk.Tk()
    app = InventoryApp(root, inventory, transactions, reports, str(DATA_FILE))
    root.mainloop()


if __name__ == "__main__":
    main()
