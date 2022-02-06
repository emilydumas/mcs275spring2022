"""Debugging challenge: Vending machine simulator"""
# MCS 275 Spring 2022

# This has a bug: Try buying an item costing $1.10 after depositing
# $1.15 using at least one nickel.
# That is, enter commands
# q
# q
# q
# q
# n
# n
# n
# 4
# Expected: Cheese on crackers dispensed, one nickel given as change
# Actual: Infinite loop

import sys

# Mapping from coin add commands to values (in dollars)
coin_values = { 
    "quarter": 0.25,
    "q": 0.25,
    "dime": 0.10,
    "d": 0.10,
    "nickel": 0.05,
    "n": 0.05
}

# Starting inventory.  Prices in dollars.
inventory = [
    { "stock":6, "price": 1.25, "name": "Cheesy dibbles" },
    { "stock":8, "price": 1.30, "name": "Slice of cake" },
    { "stock":10, "price": 0.75, "name": "1 kg trimethyl orthoformate" },
    { "stock":5, "price": 1.50, "name": "Single leaf of lettuce" },
    { "stock":5, "price": 1.10, "name": "\u00C9poisses on rye crackers" },
    { "stock":7, "price": 0.90, "name": "Lunar water" },
]


def dispense_change(cents):
    """print lines to simulate return of `cents` cents"""
    while cents >= 0.25:
        print("RETURN: quarter")
        cents = cents - 0.25
    while cents >= 0.10:
        print("RETURN: dime")
        cents = cents - 0.10
    while cents != 0:
        print("RETURN: nickel")
        cents = cents - 0.05


def show_inventory(inventory):
    """Display the `inventory` (list of dicts) in the format required by 
    the project description
    """
    for idx,itemdata in enumerate(inventory):
        print(idx,itemdata["name"],
              "${:.2f} ({} available)".format(itemdata["price"],
                                              itemdata["stock"]))


def vend(inventory):
    """Run the vending machine simulator with a given `inventory`."""    

    # Determine the maximum price of an item
    maxprice = 0
    for d in inventory:
        if d["price"] > maxprice:
            maxprice = d["price"]

    invitems = [ str(x) for x in range(len(inventory)) ]
    print("Welcome to the vending machine.  Enter command 'h' for help.")

    # Command loop
    credit = 0.0
    while True:
        print("CREDIT: ${:.2f}".format(credit))
        cmd = input(">")

        if cmd in ["q","d","n","quarter","dime","nickel"]:
            # Coin inserted
            if credit >= maxprice:
                print("RETURN:",cmd)
            else:
                credit = credit + coin_values[cmd]
        elif cmd in invitems:
            # Snack purchase request
            i = int(cmd)  # 0-based index
            if inventory[i]["stock"] == 0:
                print("MSG: Out of stock")
            elif credit < inventory[i]["price"]:
                print("MSG: Insufficient credit")
            else:
                inventory[i]["stock"] = inventory[i]["stock"] - 1
                print("VEND:",inventory[i]["name"])
                dispense_change(credit - inventory[i]["price"])
                credit = 0
        elif cmd in ["inventory","i"]:
            # Request to display inventory
            show_inventory(inventory)
        elif cmd in ["return","r"]:
            # Return current credit
            dispense_change(credit)
            credit = 0
        elif cmd in ["help","h"]:
            # Display help
            print("Vending machine simulator knows about these commands:")
            print("h or help - show this message")
            print("i or inventory - show numbered list of items available for purchase")
            print("q or quarter - deposit a quarter ($0.25)")
            print("d or dime - deposit a dime ($0.10)")
            print("n or nickel - deposit a nickel ($0.05)")
            print("r or return - return all credit currently in machine")
            print("0, 1, 2, ... - buy an item by number")
        elif cmd == "exit":
            # exit the simulation
            return
        else:
            # Unknown command
            print("Unknown command: {}".format(cmd))


if __name__ == "__main__":
    # Start the simulation.
    vend(inventory)
