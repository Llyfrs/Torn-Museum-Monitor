#!/usr/bin/python3


import requests
import time
import math
import os
from colorama import init, Fore, Back, Style
from collections import namedtuple 
init(autoreset=True)

API_key = ""




Collectible = namedtuple('Collectible',['name','quantity','market_price','place'],defaults=(None,))



def get_request(url):
    json_info = requests.get(url).json()
    
    while True:
            if json_info.get("error") == None:
                break
            time.sleep(5)
            json_info = requests.get(url).json()
    return json_info



point_amount = 10

Plushies = ["Jaguar Plushie", "Lion Plushie", "Panda Plushie", "Monkey Plushie", "Chamois Plushie" , "Wolverine Plushie", "Nessie Plushie", "Red Fox Plushie", "Camel Plushie", "Kitten Plushie", "Teddy Bear Plushie", "Sheep Plushie", "Stingray Plushie"]
Plushies_Place = ["Mexico","Africa","China","Argentina","Switzerland","Canada","United Kingdom","United Kingdom","United Arabian","Torn","Torn","Torn","Cayman Islands"]

Flowers = ["Dahlia","Orchid","African Violet","Cherry Blossom","Peony","Ceibo Flower","Edelweiss","Crocus","Heather","Tribulus Omanense","Banana Orchid"]

choice = input("1. Plushies \n2. Flowers\n:")

if choice == "1":
    museum_set = Plushies
    pass
elif choice == "2":
    museum_set = Flowers
    pass

del(choice)

while(True):

    Collectibles = list()

    inventory = get_request("https://api.torn.com/user/?selections=inventory&key={}".format(API_key)).get("inventory")

    items = get_request("https://api.torn.com/torn/?selections=items&key=" + API_key).get("items")

    for i, collectible in enumerate(museum_set):
        if collectible in str(inventory):
            for item in inventory:
                if item.get("name") == collectible:
                    Collectibles.append(Collectible(collectible,item.get("quantity"),item.get("market_price"),Plushies_Place[i]))
                    pass
        else:

            for item in items:
                item = items.get(item)
                if item.get("name") == collectible:
                    Collectibles.append(Collectible(collectible,0,item.get("market_value"),Plushies_Place[i]))



        pass

    del(items)
    del(inventory)



    top_amount = 0
    min_amount = 1000

    for item in Collectibles:
        if item.quantity > top_amount:
            top_amount = item.quantity
        if item.quantity < min_amount:
            min_amount = item.quantity


    os.system("clear")


    one_set_cost_complete = 0
    max_set_cost_complete = 0




    one_set_cost_market = 0
    max_set_cost_market = 0
    current_set_cost_market = 0

    for item in Collectibles:
        
        one_set_cost_market += item.market_price
        max_set_cost_market += item.market_price * top_amount
        current_set_cost_market += item.market_price * min_amount


        
        quantity = item.quantity

        if quantity == 0:
            one_set_cost_complete += item.market_price
            pass

        if quantity != top_amount:
            max_set_cost_complete += (top_amount-quantity) * item.market_price
            pass
        

        R = round(144 * (quantity/float(top_amount)))
        if quantity !=0 : R += 60
        c = "\033[38;2;{};{};100m".format(255 - R, 51 + R)

        report = c + "[" + str(quantity) + "]" + item.name + "\033[0m "

        print(report)


    points = get_request("https://api.torn.com/market/?selections=pointsmarket&key="+API_key).get("pointsmarket")

    point_value = 0

    for point in points:
        point_value = points.get(point).get("cost")
        break

    del(points)

    one_set_cost_museum = point_value * point_amount
    max_set_cost_museum = point_value * point_amount * top_amount
    current_set_cost_museum = point_value * point_amount * min_amount

    #Final report 

    print("\nOne set:")
    print("     Cost to complete:"+Fore.GREEN+" ${:,}".format(one_set_cost_complete))
    print("     Worth on market: ${:,}".format(one_set_cost_market))
    print("     Worth in museum: ${:,}".format(one_set_cost_museum))
    difference = one_set_cost_museum - one_set_cost_market
    if difference >= 0: print("     Difference:"+ Fore.GREEN + " ${:,}".format(difference))
    else: print("     Difference:"+ Fore.RED + " ${:,}".format(difference))


    print("\nMax set:")
    print("     Cost to complete:"+ Fore.GREEN +" ${:,}".format(max_set_cost_complete))
    print("     Worth on market: ${:,}".format(max_set_cost_market))
    print("     Worth in museum: ${:,}".format(max_set_cost_museum))
    difference = max_set_cost_museum - max_set_cost_market
    if difference >= 0: print("     Difference:"+ Fore.GREEN + " ${:,}".format(difference))
    else: print("     Difference:"+ Fore.RED + " ${:,}".format(difference))

    if min_amount != 0:
        print("\nCurrent set [{}] :".format(min_amount))
        print("     Worth on market: ${:,}".format(current_set_cost_market))
        print("     Worth in museum: ${:,}".format(current_set_cost_museum))
        difference = current_set_cost_museum - current_set_cost_market
        if difference >= 0: print("     Difference:"+ Fore.GREEN + " ${:,}".format(difference))
        else: print("     Difference:"+ Fore.RED + " ${:,}".format(difference))

        print("\n https://www.torn.com/museum.php \n")
    
    time.sleep(30)
