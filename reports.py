from collections import defaultdict
from datetime import datetime
from transactions import TransactionManager


class ReportManager:
    def __init__(self, transaction_manager: TransactionManager) -> None:
        self.transaction_manager = transaction_manager

    def _transactions(self) -> list:
        return self.transaction_manager.load_transactions()

    def total_sales_revenue(self) -> float:
        return round(
            sum(t["total"] for t in self._transactions() if t["type"] == "sale"), 2
        )

    def total_purchase_value(self) -> float:
        return round(
            sum(t["total"] for t in self._transactions() if t["type"] == "purchase"), 2
        )

    def sales_count(self) -> int:
        return sum(1 for t in self._transactions() if t["type"] == "sale")

    def purchase_count(self) -> int:
        return sum(1 for t in self._transactions() if t["type"] == "purchase")

    def most_sold_product(self):
        sold = defaultdict(int)
        for t in self._transactions():
            if t["type"] == "sale":
                sold[t["product"]] += t["quantity"]

        if not sold:
            return None, 0

        product, qty = max(sold.items(), key=lambda item: item[1])
        return product, qty

    def daily_revenue(self) -> dict[str, float]:
        revenue = defaultdict(float)
        for t in self._transactions():
            if t["type"] == "sale":
                day = t["date"].split()[0]
                revenue[day] += t["total"]

        return {day: round(total, 2) for day, total in sorted(revenue.items())}

    def today_revenue(self) -> float:
        today = datetime.now().strftime("%Y-%m-%d")
        return round(self.daily_revenue().get(today, 0.0), 2)

    def print_summary_report(self) -> None:
        top_product, top_qty = self.most_sold_product()

        print("\n" + "=" * 45)
        print("Inventory Business Report")
        print("=" * 45)
        print(f"Total sales revenue     : €{self.total_sales_revenue():.2f}")
        print(f"Total purchase value    : €{self.total_purchase_value():.2f}")
        print(f"Sales transactions      : {self.sales_count()}")
        print(f"Purchase transactions   : {self.purchase_count()}")
        if top_product:
            print(f"Most sold product       : {top_product} ({top_qty} units)")
        else:
            print("Most sold product       : No sales yet")
        print(f"Today's revenue         : €{self.today_revenue():.2f}")
        print("=" * 45)

    def print_daily_revenue_report(self) -> None:
        revenue = self.daily_revenue()
        if not revenue:
            print("\nNo sales data available yet.")
            return

        print("\n" + "=" * 35)
        print("Daily Revenue Report")
        print("=" * 35)
        for day, total in revenue.items():
            print(f"{day} : €{total:.2f}")
        print("=" * 35)
