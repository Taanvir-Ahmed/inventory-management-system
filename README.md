# Inventory Management System

A beginner-friendly Python command-line project for managing store inventory. The program reads product data from a text file, lets the user view and update inventory, and saves changes back to the file.

## Features

- Read inventory data from a `.txt` file
- Display inventory in a neat table
- Add new products
- Update stock quantities
- Update product prices
- Search products by keyword
- Show low-stock items
- Save updated data back to file
- Input validation and basic error handling

## Technologies Used

- Python 3
- Text file handling
- Dictionaries
- Functions
- Loops and conditionals

## Project Structure

- `inventory_management_system.py` → main Python program
- `inventory_data.txt` → sample inventory data

## Sample Data Format

Each line in the text file follows this format:

`Product Name: quantity: price`

Example:

`Apple: 50: 0.99`

## How to Run

1. Make sure Python 3 is installed.
2. Place `inventory_management_system.py` and `inventory_data.txt` in the same folder.
3. Open terminal in that folder.
4. Run:

```bash
python inventory_management_system.py
```

## Skills Demonstrated

This project shows:

- file reading and writing
- working with dictionaries
- modular programming
- input validation
- command-line interface design
- problem solving with Python

## Ideas for Future Improvement

- convert the project to use classes
- store data in CSV or JSON
- add sales and purchase history
- create a graphical user interface with Tkinter
- connect the project to a database
