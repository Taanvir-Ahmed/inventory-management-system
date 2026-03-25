from __future__ import annotations

from pathlib import Path
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

from inventory import Inventory
from product import Product
from reports import ReportManager
from transactions import TransactionManager


class InventoryApp:
    def __init__(
        self,
        root: tk.Tk,
        inventory: Inventory,
        transactions: TransactionManager,
        reports: ReportManager,
        data_file: str,
    ) -> None:
        self.root = root
        self.inventory = inventory
        self.transactions = transactions
        self.reports = reports
        self.data_file = data_file

        self.root.title("Inventory Management System")
        self.root.geometry("900x560")
        self.root.minsize(850, 520)

        self._build_ui()
        self.refresh_inventory()

    def _build_ui(self) -> None:
        title = ttk.Label(
            self.root,
            text="Inventory Management System",
            font=("Arial", 18, "bold"),
        )
        title.pack(pady=(15, 8))

        button_frame = ttk.Frame(self.root)
        button_frame.pack(fill="x", padx=20, pady=(0, 10))

        buttons = [
            ("Add Product", self.add_product_dialog),
            ("Restock", self.restock_dialog),
            ("Sell", self.sell_dialog),
            ("Update Price", self.update_price_dialog),
            ("Search", self.search_dialog),
            ("Low Stock", self.low_stock_dialog),
            ("Transactions", self.show_transactions_window),
            ("Reports", self.show_reports_window),
            ("Save", self.save_inventory),
            ("Refresh", self.refresh_inventory),
        ]

        for i, (label, command) in enumerate(buttons):
            ttk.Button(button_frame, text=label, command=command).grid(
                row=i // 5, column=i % 5, padx=5, pady=5, sticky="ew"
            )

        for col in range(5):
            button_frame.columnconfigure(col, weight=1)

        table_frame = ttk.Frame(self.root)
        table_frame.pack(fill="both", expand=True, padx=20, pady=10)

        columns = ("product_id", "name", "quantity", "price", "value")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=18)

        self.tree.heading("product_id", text="ID")
        self.tree.heading("name", text="Name")
        self.tree.heading("quantity", text="Quantity")
        self.tree.heading("price", text="Price (€)")
        self.tree.heading("value", text="Value (€)")

        self.tree.column("product_id", width=100, anchor="center")
        self.tree.column("name", width=260)
        self.tree.column("quantity", width=100, anchor="center")
        self.tree.column("price", width=120, anchor="center")
        self.tree.column("value", width=120, anchor="center")

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        footer = ttk.Frame(self.root)
        footer.pack(fill="x", padx=20, pady=(0, 15))
        ttk.Button(footer, text="Exit", command=self.on_exit).pack(side="right")

    def refresh_inventory(self) -> None:
        for row in self.tree.get_children():
            self.tree.delete(row)

        for product in self.inventory.products.values():
            value = product.quantity * product.price
            self.tree.insert(
                "",
                "end",
                values=(
                    product.product_id,
                    product.name,
                    product.quantity,
                    f"{product.price:.2f}",
                    f"{value:.2f}",
                ),
            )

    def _ask_non_negative_int(self, prompt: str, title: str = "Input") -> int | None:
        while True:
            value = simpledialog.askstring(title, prompt, parent=self.root)
            if value is None:
                return None
            try:
                parsed = int(value)
                if parsed < 0:
                    raise ValueError
                return parsed
            except ValueError:
                messagebox.showerror("Invalid Input", "Please enter a non-negative whole number.")

    def _ask_non_negative_float(self, prompt: str, title: str = "Input") -> float | None:
        while True:
            value = simpledialog.askstring(title, prompt, parent=self.root)
            if value is None:
                return None
            try:
                parsed = float(value)
                if parsed < 0:
                    raise ValueError
                return parsed
            except ValueError:
                messagebox.showerror("Invalid Input", "Please enter a non-negative number.")

    def add_product_dialog(self) -> None:
        product_id = simpledialog.askstring("Add Product", "Enter product ID:", parent=self.root)
        if product_id is None:
            return
        product_id = product_id.strip()

        name = simpledialog.askstring("Add Product", "Enter product name:", parent=self.root)
        if name is None:
            return
        name = name.strip()

        if not product_id or not name:
            messagebox.showerror("Error", "Product ID and name cannot be empty.")
            return

        quantity = self._ask_non_negative_int("Enter quantity:", "Add Product")
        if quantity is None:
            return
        price = self._ask_non_negative_float("Enter price (€):", "Add Product")
        if price is None:
            return

        product = Product(product_id, name, quantity, price)
        if self.inventory.add_product(product):
            self.refresh_inventory()
            messagebox.showinfo("Success", f"Product '{name}' added successfully.")
        else:
            messagebox.showerror("Error", f"A product with ID '{product_id}' already exists.")

    def restock_dialog(self) -> None:
        product_id = simpledialog.askstring("Restock Product", "Enter product ID:", parent=self.root)
        if product_id is None:
            return
        product = self.inventory.find_by_id(product_id.strip())
        if product is None:
            messagebox.showerror("Error", "Product not found.")
            return

        amount = self._ask_non_negative_int("Enter quantity to add:", "Restock Product")
        if amount is None:
            return

        if self.inventory.restock_product(product.product_id, amount):
            self.transactions.add_transaction("purchase", product.name, amount, product.price)
            self.refresh_inventory()
            messagebox.showinfo("Success", "Product restocked successfully.")

    def sell_dialog(self) -> None:
        product_id = simpledialog.askstring("Sell Product", "Enter product ID:", parent=self.root)
        if product_id is None:
            return
        product = self.inventory.find_by_id(product_id.strip())
        if product is None:
            messagebox.showerror("Error", "Product not found.")
            return

        amount = self._ask_non_negative_int("Enter quantity to sell:", "Sell Product")
        if amount is None:
            return

        if self.inventory.sell_product(product.product_id, amount):
            self.transactions.add_transaction("sale", product.name, amount, product.price)
            self.refresh_inventory()
            messagebox.showinfo("Success", "Sale completed successfully.")
        else:
            messagebox.showerror(
                "Error", f"Not enough stock. Available quantity: {product.quantity}"
            )

    def update_price_dialog(self) -> None:
        product_id = simpledialog.askstring("Update Price", "Enter product ID:", parent=self.root)
        if product_id is None:
            return
        product = self.inventory.find_by_id(product_id.strip())
        if product is None:
            messagebox.showerror("Error", "Product not found.")
            return

        price = self._ask_non_negative_float("Enter new price (€):", "Update Price")
        if price is None:
            return

        if self.inventory.update_price(product.product_id, price):
            self.refresh_inventory()
            messagebox.showinfo("Success", "Price updated successfully.")

    def search_dialog(self) -> None:
        keyword = simpledialog.askstring("Search Product", "Enter product name or keyword:", parent=self.root)
        if keyword is None:
            return
        matches = self.inventory.search_by_name(keyword)
        if not matches:
            messagebox.showinfo("Search", "No matching products found.")
            return

        lines = [
            f"{p.product_id} - {p.name} | Qty: {p.quantity} | Price: €{p.price:.2f}"
            for p in matches
        ]
        self._show_text_window("Search Results", "\n".join(lines), width=700, height=300)

    def low_stock_dialog(self) -> None:
        threshold = self._ask_non_negative_int("Enter low-stock threshold:", "Low Stock Report")
        if threshold is None:
            return
        low_stock = self.inventory.low_stock_products(threshold)
        if not low_stock:
            messagebox.showinfo("Low Stock Report", "All products are sufficiently stocked.")
            return

        lines = [f"{p.product_id} - {p.name}: {p.quantity} units" for p in low_stock]
        self._show_text_window("Low Stock Report", "\n".join(lines), width=500, height=300)

    def show_transactions_window(self) -> None:
        transactions = self.transactions.load_transactions()
        if not transactions:
            messagebox.showinfo("Transactions", "No transactions found.")
            return

        lines = []
        for t in transactions:
            lines.append(
                f"{t['date']} | {t['type'].upper():<8} | {t['product']:<20} | "
                f"Qty: {t['quantity']:<4} | Price: €{t['price']:.2f} | Total: €{t['total']:.2f}"
            )
        self._show_text_window("Transaction History", "\n".join(lines), width=900, height=350)

    def show_reports_window(self) -> None:
        top_product, top_qty = self.reports.most_sold_product()
        report_text = (
            "Inventory Business Report\n"
            "=" * 32
            + f"\nTotal sales revenue   : €{self.reports.total_sales_revenue():.2f}"
            + f"\nTotal purchase value  : €{self.reports.total_purchase_value():.2f}"
            + f"\nSales transactions    : {self.reports.sales_count()}"
            + f"\nPurchase transactions : {self.reports.purchase_count()}"
            + (
                f"\nMost sold product     : {top_product} ({top_qty} units)"
                if top_product
                else "\nMost sold product     : No sales yet"
            )
            + f"\nToday's revenue       : €{self.reports.today_revenue():.2f}"
            + "\n\nDaily Revenue\n"
            + "-" * 32
        )

        daily = self.reports.daily_revenue()
        if daily:
            for day, total in daily.items():
                report_text += f"\n{day}: €{total:.2f}"
        else:
            report_text += "\nNo sales data available yet."

        self._show_text_window("Reports", report_text, width=650, height=420)

    def _show_text_window(self, title: str, content: str, width: int = 600, height: int = 400) -> None:
        window = tk.Toplevel(self.root)
        window.title(title)
        window.geometry(f"{width}x{height}")

        text = tk.Text(window, wrap="word")
        scrollbar = ttk.Scrollbar(window, orient="vertical", command=text.yview)
        text.configure(yscrollcommand=scrollbar.set)

        text.insert("1.0", content)
        text.config(state="disabled")

        text.pack(side="left", fill="both", expand=True, padx=(10, 0), pady=10)
        scrollbar.pack(side="right", fill="y", padx=(0, 10), pady=10)

    def save_inventory(self) -> None:
        self.inventory.save_to_csv(self.data_file)
        messagebox.showinfo("Saved", f"Inventory saved to '{Path(self.data_file).name}'.")

    def on_exit(self) -> None:
        self.inventory.save_to_csv(self.data_file)
        self.root.destroy()
