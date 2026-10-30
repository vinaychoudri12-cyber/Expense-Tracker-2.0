
import csv
import os
from datetime import datetime

FILE_NAME = "expenses.csv"

# Create CSV file with headers if it doesn't exist
def initialize_file():
    if not os.path.exists(FILE_NAME) or os.path.getsize(FILE_NAME) == 0:
        with open(FILE_NAME, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Date", "Item", "Amount", "Category"])


# Add a new expense
def add_expense():
    print("\n--- Add Expense ---")

    item = input("Enter expense name: ").strip()
    if not item:
        print("Expense name cannot be empty.")
        return

    try:
        amount = float(input("Enter amount: "))
        if amount <= 0:
            print("Amount must be greater than zero.")
            return
    except ValueError:
        print("Please enter a valid amount.")
        return

    category = input("Enter category (Food/Travel/Shopping): ").strip()
    if not category:
        print("Category cannot be empty.")
        return

    date_input = input("Enter date (YYYY-MM-DD) or press Enter for today: ").strip()

    if date_input:
        try:
            expense_date = datetime.strptime(
                date_input, "%Y-%m-%d"
            ).date().isoformat()
        except ValueError:
            print("Invalid date format.")
            return
    else:
        expense_date = datetime.today().date().isoformat()

    with open(FILE_NAME, "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([expense_date, item, amount, category.title()])

    print("Expense added successfully!")


# Read all expenses
def read_expenses():
    with open(FILE_NAME, "r", newline="") as file:
        return list(csv.DictReader(file))


# Display expenses
def display_expenses(expenses):
    if not expenses:
        print("No expenses found.")
        return

    print("\nDate         Item             Amount       Category")
    print("-" * 60)

    for expense in expenses:
        print(
            f"{expense['Date']:<13}"
            f"{expense['Item']:<17}"
            f"₹{float(expense['Amount']):<11.2f}"
            f"{expense['Category']}"
        )


# Search expenses by category
def search_by_category():
    category = input("\nEnter category to search: ").strip()

    if not category:
        print("Category cannot be empty.")
        return

    expenses = read_expenses()

    matching = [
        expense for expense in expenses
        if expense["Category"].lower() == category.lower()
    ]

    print(f"\nExpenses in category: {category}")
    display_expenses(matching)


# Calculate total spending per category
def category_totals():
    expenses = read_expenses()
    totals = {}

    for expense in expenses:
        category = expense["Category"]
        amount = float(expense["Amount"])

        totals[category] = totals.get(category, 0) + amount

    print("\n--- Category-wise Spending ---")

    if not totals:
        print("No expenses available.")
        return

    for category, total in totals.items():
        print(f"{category}: ₹{total:.2f}")


# Calculate monthly spending
def monthly_total():
    month = input("\nEnter month (YYYY-MM): ").strip()

    try:
        datetime.strptime(month, "%Y-%m")
    except ValueError:
        print("Invalid month. Use YYYY-MM format.")
        return

    expenses = read_expenses()

    total = sum(
        float(expense["Amount"])
        for expense in expenses
        if expense["Date"].startswith(month)
    )

    print(f"\nTotal spending for {month}: ₹{total:.2f}")


# Main menu
def main():
    initialize_file()

    while True:
        print("\n========== EXPENSE TRACKER 2.0 ==========")
        print("1. Add Expense")
        print("2. View All Expenses")
        print("3. Search Expenses by Category")
        print("4. Category-wise Total Spending")
        print("5. Monthly Spending")
        print("6. Exit")

        choice = input("\nEnter your choice (1-6): ").strip()

        if choice == "1":
            add_expense()
        elif choice == "2":
            display_expenses(read_expenses())
        elif choice == "3":
            search_by_category()
        elif choice == "4":
            category_totals()
        elif choice == "5":
            monthly_total()
        elif choice == "6":
            print("Thank you for using Expense Tracker 2.0!")
            break
        else:
            print("Invalid choice. Please select 1-6.")


if __name__ == "__main__":
    main()

