# Inventory Management System

A Python-based inventory management application that demonstrates object-oriented programming, file handling, data analysis, and graphical user interface development.

This project evolved step-by-step from a simple command-line tool into a full-featured application with reporting and a Tkinter GUI.

---

## Features

### Core Functionality

* Add new products
* Update stock quantity
* Restock products
* Sell products
* Update product prices
* Search products by name
* Display inventory in a structured format
* Low-stock alerts

### Data Management

* Inventory stored using CSV files
* Transactions stored using JSON
* Persistent data across sessions

### Transaction System

* Records every sale and restock
* Stores date, type, quantity, and total value
* View complete transaction history

### Reports & Analytics

* Total sales revenue
* Total purchase value
* Number of sales and purchase transactions
* Most sold product
* Daily revenue tracking

### Graphical User Interface (GUI)

* Built with Tkinter
* Interactive buttons and forms
* Inventory displayed in a table
* Separate views for transactions and reports

---

## Project Structure

```id="struct01"
inventory-management-system/
├── main.py              # Launches GUI
├── main_cli.py          # (Optional) CLI version
├── gui.py               # Tkinter interface
├── product.py           # Product class
├── inventory.py         # Inventory logic
├── transactions.py      # Transaction management
├── reports.py           # Business analytics
├── inventory_data.csv   # Inventory data
├── transactions.json    # Transaction history
├── README.md
└── .gitignore
```

---

## Technologies Used

* Python
* Object-Oriented Programming (OOP)
* CSV file handling
* JSON data storage
* Tkinter (GUI development)

---

## How to Run

### Run GUI version (recommended)

```id="run01"
python main.py
```

or (Mac/Linux):

```id="run02"
python3 main.py
```

### Run CLI version (optional)

```id="run03"
python main_cli.py
```

---

## Example Features in Action

### Inventory Management

* Add, update, and track products easily
* Automatically saves changes to CSV

### Transaction Tracking

* Every sale and restock is recorded
* Stored in JSON format for analysis

### Reports

* View business insights such as revenue and most sold items
* Helps simulate real-world inventory decision making

---

## Project Evolution

* **Version 1**

  * Basic command-line inventory system
  * Used text file storage

* **Version 2**

  * Refactored into object-oriented design
  * Introduced Product and Inventory classes

* **Version 3**

  * Switched data storage from text file to CSV

* **Version 4**

  * Added transaction tracking using JSON

* **Version 5**

  * Implemented business reports and analytics
  * Built a Tkinter graphical user interface

---

## Future Improvements

* Export reports to CSV or Excel
* Add user authentication system
* Improve GUI styling and layout
* Deploy as a desktop application

---

## Author

Tanvir Ahmed
