#!/usr/bin/python3

import requests
import time
import os
from colorama import init, Fore, Back, Style
from collections import namedtuple

init(autoreset=True)

API_key = ""  # Here comes your API key

if API_key == "":  # In case user doesn't want to edit code.
    print("You are missing API key, pleas enter it. \nIf you don't want to enter your key every time you run the "
          "program you can insert it to the code and this message will get skiped")
    API_key = input("Your API key:")

# Structure to hold multiple information in one variable/object The object holds name of the item the amount of the
# item in users inventory market price of the item and place where you can buy this item for example you can buy
# Monkey Plushie in UK

Collectible = namedtuple('Collectible', ['name', 'quantity', 'market_price', 'place'], defaults=(None,))


def get_request(url):
    while True:
        try:
            json_info = requests.get(url).json()
            if not json_info.get("error"):
                return json_info
        except requests.exceptions.RequestException as e:
            print(e)
            time.sleep(5)


def print_set(name: str, set_market_cost: int, set_museum_cost: int, cost_to_complete: int = 0):
    print(f"\n\n{name}:")
    if cost_to_complete != 0:
        print("     Cost to complete:" + Fore.GREEN + " ${:,}".format(cost_to_complete))
    print("     Worth on market: ${:,}".format(set_market_cost))
    print("     Worth in museum: ${:,}".format(set_museum_cost))
    print("     Worth on M-day:  ${:,}".format(round(set_museum_cost * 1.1)))
    diff = set_museum_cost - set_market_cost
    mday_diff = round(set_museum_cost * 1.1) - set_market_cost
    if diff >= 0:
        print("     Difference:" + Fore.GREEN + "  ${:,}".format(diff))
    else:
        print("     Difference:" + Fore.RED + "  ${:,}".format(diff))

    if mday_diff >= 0:
        print("     M-day Diffr:" + Fore.GREEN + " ${:,}".format(mday_diff))
    else:
        print("     M-day Diffr:" + Fore.RED + " ${:,}".format(mday_diff))

    pass


# The amount off points you get from one set right now is ten for both Plushies and Flowers but if other sets are
# added this needs to be changed accordingly
point_amount = 10

sets = list()

sets.append(
    ["Jaguar Plushie", "Lion Plushie", "Panda Plushie", "Monkey Plushie", "Chamois Plushie", "Wolverine Plushie",
     "Nessie Plushie", "Red Fox Plushie", "Camel Plushie", "Kitten Plushie", "Teddy Bear Plushie",
     "Sheep Plushie", "Stingray Plushie"])

Plushies_Place = ["Mexico", "Africa", "China", "Argentina", "Switzerland", "Canada", "United Kingdom", "United Kingdom",
                  "United Arabian", "Torn", "Torn", "Torn", "Cayman Islands"]

sets.append(["Dahlia", "Orchid", "African Violet", "Cherry Blossom", "Peony", "Ceibo Flower", "Edelweiss", "Crocus",
             "Heather", "Tribulus Omanense", "Banana Orchid"])

sets.append(["Leopard Coin", "Florin Coin", "Gold Noble Coin"])

# After coins there isn't any real reason to use this program to track the amount of items in your inventory since
# you only need to track one, but it can still tell you if is worth buying the item on the market for market price.

sets.append(["Vairocana Buddha Sculpture"])
sets.append(["Ganesha Sculpture"])
sets.append(["Shabti Sculpture"])
sets.append(["Quran Script : Ibn Masud", "Quran Script : Ubay Ibn Kab", "Quran Script : Ali"])
sets.append(["Egyptian Amulet"])

sets_rewards = [10, 10, 100, 100, 250, 500, 1000, 10000]

# Choosing witch set you want to monitor.
# If anybody knows how to write this better feal free to let me know. 
# Senet Game not included cuz it will break/make useles half of the program. 

while (True):
    choice = input(
        "1. Plushies \n2. Flowers\n3. Medieval Coins\n4. Vairocana Buddha\n5. Ganesha Sculpture\n6. Shabit "
        "Sculpture\n7. Script's from the Quran\n8. Egyptian Amulet\n:")

    choice = int(choice)
    os.system("clear")
    if 0 < choice < 9:
        museum_set = sets[choice - 1]
        point_amount = sets_rewards[choice - 1]

    else:
        print(f"{choice} is not recognized as a valid input")
        print("Pleas try again\n")
        continue
    break

while (True):  # Update loop that refershes every 30 seconds

    Collectibles = list()

    inventory = get_request("https://api.torn.com/user/?selections=inventory&key={}".format(API_key)).get("inventory")

    items = get_request("https://api.torn.com/torn/?selections=items&key=" + API_key).get("items")

    # Looks for items in you inventory and creates collectible object and adds it in to the list
    for i, collectible in enumerate(museum_set):
        if collectible in str(inventory):
            for item in inventory:
                if item.get("name") == collectible:
                    Collectibles.append(
                        Collectible(collectible, item.get("quantity"), item.get("market_price"), Plushies_Place[i]))
                    pass
        # In case user doesn't have any of the item in the inventory it needs to look up the market price in items
        # API call
        else:
            for item in items:
                item = items.get(item)
                if item.get("name") == collectible:
                    Collectibles.append(Collectible(collectible, 0, item.get("market_value"), Plushies_Place[i]))
        pass

    del (items)
    del (inventory)

    top_amount = 0  # Biggest number of one item's users owns

    # With sorting this won't be needed any more
    # but that depends on if I make sorting exceptionable or not

    for item in Collectibles:
        if item.quantity > top_amount:
            top_amount = item.quantity

    min_amount = top_amount

    for item in Collectibles:
        if item.quantity < min_amount:
            min_amount = item.quantity

    inventory_value = 0

    for item in Collectibles:
        inventory_value += item.quantity * item.market_price

    change = True

    # This sorts the items from the biggest to the smallest amount in inventory, this makes it usable on windows
    # since they don't support rgb colors. The most basic algorithm for sorting might latter use some more
    # complicated just for fun :D

    while (change):
        change = False
        for i in range(len(Collectibles) - 1):
            if Collectibles[i].quantity < Collectibles[i + 1].quantity:
                Collectibles[i], Collectibles[i + 1] = Collectibles[i + 1], Collectibles[i]
                change = True

    os.system("clear")

    one_set_cost_complete = 0
    max_set_cost_complete = 0

    one_set_cost_market = 0
    max_set_cost_market = 0
    current_set_cost_market = 0

    # This si where individual items get printed with there respected color
    for item in Collectibles:

        one_set_cost_market += item.market_price
        max_set_cost_market += item.market_price * top_amount
        current_set_cost_market += item.market_price * min_amount

        quantity = item.quantity

        if quantity == 0:
            one_set_cost_complete += item.market_price
            pass

        if quantity != top_amount:
            max_set_cost_complete += (top_amount - quantity) * item.market_price
            pass

        # This part coolors items, the more items users has the more green it gets
        # To distinguish items that user doesn't own any there is a big jum in color from 0 to 1 number of items
        R = 0
        if top_amount != 0: R = round(
            144 * (quantity / float(top_amount)))  # 144 + 60 for jump + 51 witch is the based = 255
        if quantity != 0: R += 60  # this is the jump
        c = "\033[38;2;{};{};100m".format(255 - R,
                                          51 + R)  # Determines the color, might not work on windows terminal...

        report = c + "[" + str(quantity) + "]" + item.name + "\033[0m "

        print(report)

    # Grabs the average point value.
    point_value = get_request("https://api.torn.com/torn/?selections=stats&key=" + API_key).get("stats").get(
        "points_averagecost")

    one_set_cost_museum = point_value * point_amount
    max_set_cost_museum = point_value * point_amount * top_amount
    current_set_cost_museum = point_value * point_amount * min_amount

    # Final report
    # Just a lot of text to print showing variables

    print("\nInventory Value:" + Fore.GREEN + " ${:,}".format(inventory_value))
    print("Point Price: " + Fore.GREEN + "${:,}".format(point_value))

    print_set("One set", one_set_cost_market, one_set_cost_museum, one_set_cost_complete)

    # Max Set
    print_set("Max set [{}]".format(top_amount), max_set_cost_market, max_set_cost_museum, max_set_cost_complete)
    # Current sett is only shown when you can exchange at least one set at the museum

    if min_amount != 0:

        print_set("Current set [{}] :".format(min_amount), current_set_cost_market, current_set_cost_museum)
        print("\n https://www.torn.com/museum.php \n")

    # updating the table every 30 second

    # one update makes total of 3 calls since you get two updates per minute this program takes
    # 6 API calls from the 100 available every minute (that's alright). 
    time.sleep(30)
