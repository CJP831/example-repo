# ============Class functions=================
class Shoe:
    def __init__(self, country, code, product, cost, quantity):
        self.country = country
        self.code = code
        self.product = product
        self.cost = float(cost)
        self.quantity = int(quantity)

    def get_cost(self):
        return self.cost

    def get_quantity(self):
        return self.quantity

    def __str__(self):
        return (
            f"({self.country}, {self.code}, {self.product}, "
            f"{self.cost}, {self.quantity})"
        )


# ================List=======================

shoes_list = []


# ==========External functions===============

def read_shoes_data():
    """
    Reads inventory data and creates Shoe objects,
    then they're appended to the shoes list
    """

    try:
        with open('inventory.txt', 'r', encoding="utf-8") as file:
            for line in file:
                clean_line = line.strip()
                if not clean_line:
                    continue

                split_lines = clean_line.split(",")

                if len(split_lines) == 5:
                    country, code, product, cost, quantity = split_lines

                    if (
                        cost.strip().lower() == "cost"
                        or quantity.strip().lower() == "quantity"
                    ):
                        continue

                    # Strip any currency symbols and white spaces
                    cost = cost.replace("$", "").strip()
                    quantity = quantity.strip()

                    try:
                        # Create the shoe object
                        new_shoe = Shoe(country, code, product, cost, quantity)
                        shoes_list.append(new_shoe)
                    except ValueError:
                        print(f"Skipping malformed data row: {clean_line}")
                        continue

    except FileNotFoundError:
        print("Error: inventory.txt file was not found.")


def capture_shoes():
    """
    Prompts the user for shoe details,
    creates a Shoe object; appends it to shoes_list.
    """

    print("\n--- Capture New Shoe Data ---")

    country = input("Enter the country of product: ").strip()
    code = input("Enter the product code (e.g., SKU12345): ").strip()
    product = input("Enter the product name: ").strip()

    while True:
        try:
            cost = float(input("Enter the unit cost ($): "))
            if cost < 0:
                print("Cost cannot be negative. Try again.")
                continue
            break
        except ValueError:
            print("Invalid input. Please enter a valid number for cost.")

    while True:
        try:
            quantity = int(input("Enter the stock quantity: "))
            if quantity < 0:
                print("Quantity cannot be negative. Try again.")
                continue
            break
        except ValueError:
            print("Invalid input. Please enter a whole number for quantity.")

    new_shoe = Shoe(country, code, product, cost, quantity)
    shoes_list.append(new_shoe)
    print(f"\n  {product} has been added to the shoe list.")


def view_all():
    """Prints shoe inventory."""

    if not shoes_list:
        print("The inventory is currently empty.")
        return

    print("\n--- Current Inventory ---")
    for shoe in shoes_list:
        print(shoe)


def re_stock():
    """
    Finds the shoe with the lowest quantity,
    asks the user if they want to add stock,
    updates the object, and overwrites the text file.
    """

    if not shoes_list:
        print("\nThe inventory is currently empty.")
        return

    # Find the shoe object with the lowest quantity
    lowest_shoe = min(shoes_list, key=lambda shoe: shoe.quantity)

    print("\n--- Item Restock List ---")
    print(f"Product:  {lowest_shoe.product} ({lowest_shoe.code})")
    print(f"Location: {lowest_shoe.country}")
    print(f"Current Stock: {lowest_shoe.quantity}")

    choice = input(
        "\nDo you want to restock this item? (yes/no): "
    ).strip().lower()

    if choice in ['yes', 'y']:
        while True:
            try:
                added_qty = int(input("Enter the quantity to add: "))
                if added_qty < 0:
                    print("Quantity to add cannot be negative. Try again.")
                    continue
                break
            except ValueError:
                print("Invalid input. Please enter a whole number.")

        lowest_shoe.quantity += added_qty
        print(
            f"\nCurrent '{lowest_shoe.product}' stock updated to "
            f"{lowest_shoe.quantity}.\n"
        )

        try:
            with open('inventory.txt', 'w', encoding="utf-8") as file:
                for shoe in shoes_list:
                    file.write(
                        f"{shoe.country},{shoe.code},{shoe.product},"
                        f"{shoe.cost},{shoe.quantity}\n"
                    )
            print("Inventory has been updated successfully.")
        except IOError:
            print("Error: Could not update Inventory.")
    else:
        print("Restock cancelled.")


def shoe_search():
    """
    Prompts the user for a product code and searches the shoes_list.
    Prints the details of the shoe if found.
    """

    if not shoes_list:
        print("\nThe inventory is currently empty.")
        return

    search = input("\nPlease enter the code you are searching for:\n").strip()
    found = False

    for shoe in shoes_list:
        if shoe.code.lower() == search.lower():
            print("\n--- Match Found ---")
            print(shoe)
            found = True
            break

    if not found:
        print(f"\n No product found with the code '{search}'.")

    print("\nPlease select another option from the menu below\n")


def value_per_item():
    """
    Calculates the total value for each shoe item
    (Cost * Quantity) and prints the results
    """

    if not shoes_list:
        print("\nThe inventory is currently empty.")
        return

    # Used google to see how to make the table look neater
    # when displaying values. Not originally found within lessons,
    # but thought it would more user-friendly.
    print("\n--- Current Inventory Stock Value ---")
    print(
        f"{'Product':<20} | {'Code':<10} | {'Unit Cost':<10} | "
        f"{'Quantity':<8} | {'Total Value':<12}"
    )
    print("-" * 65)

    for shoe in shoes_list:
        item_total = shoe.cost * shoe.quantity
        print(
            f"{shoe.product:<20} | {shoe.code:<10} | "
            f"${shoe.cost:<9} | {shoe.quantity:<8} | "
            f"${item_total:<11}"
        )

    print("-" * 65)


def highest_qty():
    """
    Finds the shoe object with the highest quantity in stock
    """

    if not shoes_list:
        print("\nThe inventory is currently empty.")
        return

    surplus_shoe = max(shoes_list, key=lambda shoe: shoe.quantity)
    print("\n--- Highest Quantity Item ---")
    print(f"Product: {surplus_shoe.product} ({surplus_shoe.code})")
    print(f"Current Stock: {surplus_shoe.quantity} units available.")


def main_menu():
    read_shoes_data()
    # main menu selections
    # Added emoticon for fun lol.
    while True:
        print("\nHello! \\(*^o^*)/ Welcome to the Main Menu. \n"
              "Please select from the options below:")
        print("=========================================")
        print("1. View All Inventory Items")
        print("2. Restock Lowest Stock Item")
        print("3. Search for Shoe by Code")
        print("4. Check Total Value of Products")
        print("5. Find Highest Quantity Item")
        print("6. Capture & Add New Shoe Type")
        print("7. Exit Program")
        print("=========================================")
        print("\n")

        choice = input("Please select an option (1-8): ").strip()

        if choice == '1':
            view_all()
        elif choice == '2':
            re_stock()
        elif choice == '3':
            shoe_search()
        elif choice == '4':
            value_per_item()
        elif choice == '5':
            highest_qty()
        elif choice == '6':
            capture_shoes()
        elif choice == '7':
            print("\nExiting program. Goodbye!")
            break
        else:
            print("\n Invalid selection. Please enter a number from 1 to 8.")


# Launches the menu
if __name__ == "__main__":
    main_menu()
