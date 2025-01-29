# first, import the library
import pandas as pd

#  inventory with the quantity and prices
inv = {
    "apple": {"quantity": 3, "price": 1.5},
    "banana": {"quantity": 6, "price": 0.5},
    "orange": {"quantity": 4, "price": 1.0},
    "grapes": {"quantity": 10, "price": 2.0},
    "mango": {"quantity": 2, "price": 1.8},
    "pineapple": {"quantity": 1, "price": 3.0},
    "watermelon": {"quantity": 1, "price": 5.0},
    "strawberry": {"quantity": 5, "price": 1.2},
}


# for the add iteams
def add_item():
    item = input("Enter the item name: ").strip().lower()

    while True:
        try:
            quantity = int(input("Enter the quantity: "))
            if quantity <= 0:
                print("Quantity must be a positive number. Try again.")
                continue
            break
        except ValueError:
            print("Invalid input! Please enter a valid number.")

    while True:
        try:
            price = float(input("Enter the price per unit: "))
            if price <= 0:
                print("Price must be a positive number. Try again.")
                continue
            break
        except ValueError:
            print("Invalid input! Please enter a valid price.")

    if item in inv:
        inv[item]["quantity"] += quantity
    else:
        inv[item] = {"quantity": quantity, "price": price}

    print(f"{quantity} {item}(s) added to inventory at ${price:.2f} each.")


# for the search items
def search_item():
    item = input("Enter the item name to search: ").strip().lower()
    if item in inv:
        print(
            f"{item.capitalize()} - Quantity: {inv[item]['quantity']}, Price: ${inv[item]['price']:.2f}"
        )
    else:
        print(f"Error: '{item}' is not found in the inventory.")


# For the display
def display_inventory():
    if not inv:
        print("The inventory is currently empty.")
        return

    df_inventory = pd.DataFrame.from_dict(inv, orient="index").reset_index()
    df_inventory.columns = ["Item", "Quantity", "Price"]
    print("\nCurrent Inventory:")
    print(df_inventory.to_string(index=False))


while True:
    print("\nChoose an action:")
    print("1. Add new item")
    print("2. Search for an item")
    print("3. Display the inventory")
    print("4. Exit from the inventory management system")

    choice = input("Enter your choice (1-4): ").strip()

    if choice == "1":
        add_item()
    elif choice == "2":
        search_item()
    elif choice == "3":
        display_inventory()
    elif choice == "4":
        break
    else:
        print("Invalid choice! Please enter a number between 1 and 4.")

    # As asked, Program ends after the last questionwhile True:
    view_inventory = (
        input("\nDo you want to see the whole inventory? (yes/no): ").strip().lower()
    )
    if view_inventory == "yes":
        display_inventory()
        break
    elif view_inventory == "no":
        print("Inventory display skipped.")
        break
    else:
        print("Invalid input! Please enter 'yes' or 'no'.")


print("\nThank you for using the Inventory Management System. Goodbye!")
