#!/usr/bin/python3


import requests
import time
import math
import os
from colorama import init, Fore, Back, Style
from collections import namedtuple 
init(autoreset=True)

API_key = "" #Here comes your API key 

if API_key == "": #In case user doesn't want to edit code. 
    print("You are missing API key, pleas enter it. \nIf you don't want to enter your key every time you run the program you can insert it to the code and this message will get skiped")
    API_key = input("Your API key:")


#Structure to hold multiple information in one variable/object
#The object holds name of the item the amount of the item in users inventory market price of the item and place where you can buy this item
#for example you can buy Monkey Plushie in UK 

Collectible = namedtuple('Collectible',['name','quantity','market_price','place'],defaults=(None,)) 

def get_request(url): #Code that waits and retryes request when error occurs (most comonly running out off AP calls) 
    json_info = requests.get(url).json()
    
    while True:
            if json_info.get("error") == None:
                break
            time.sleep(5)
            json_info = requests.get(url).json()
    return json_info

point_amount = 10 #The amount off points you get from one set right now is ten for both Plushies and Flowers but if other sets are added this needs to be changed accordingly

Plushies = ["Jaguar Plushie", "Lion Plushie", "Panda Plushie", "Monkey Plushie", "Chamois Plushie" , "Wolverine Plushie", "Nessie Plushie", "Red Fox Plushie", "Camel Plushie", "Kitten Plushie", "Teddy Bear Plushie", "Sheep Plushie", "Stingray Plushie"]

Plushies_Place = ["Mexico","Africa","China","Argentina","Switzerland","Canada","United Kingdom","United Kingdom","United Arabian","Torn","Torn","Torn","Cayman Islands"]

Flowers = ["Dahlia","Orchid","African Violet","Cherry Blossom","Peony","Ceibo Flower","Edelweiss","Crocus","Heather","Tribulus Omanense","Banana Orchid"]

# Choosin witch set you want to monitor.
choice = input("1. Plushies \n2. Flowers\n:")

if choice == "1":
    museum_set = Plushies
    pass
elif choice == "2":
    museum_set = Flowers
    pass

del(choice)
del(Plushies)
del(Flowers)

while(True): #Update loop that refershes every 30 seconds

    Collectibles = list()

    inventory = get_request("https://api.torn.com/user/?selections=inventory&key={}".format(API_key)).get("inventory")

    items = get_request("https://api.torn.com/torn/?selections=items&key=" + API_key).get("items")

    for i, collectible in enumerate(museum_set): # Looks for items in you inventory and creates collectible object and adds it in to the list 
        if collectible in str(inventory):
            for item in inventory:
                if item.get("name") == collectible:
                    Collectibles.append(Collectible(collectible,item.get("quantity"),item.get("market_price"),Plushies_Place[i]))
                    pass
        else: # in case user doesn't have any of the item in the inventory it needs to look up the market price in items API call 

            for item in items:
                item = items.get(item)
                if item.get("name") == collectible:
                    Collectibles.append(Collectible(collectible,0,item.get("market_value"),Plushies_Place[i]))
        pass

    del(items)
    del(inventory)

    top_amount = 0 #Biggest number of one items users owns 
    min_amount = 1000 # must start on a big number. Shows the lowest number of items user owns if not 0 that means user can exchange at leas one set 

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

    #This si where individual items get printed with there respected color 
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
        
        #This part coolors items, the more items users has the more green it gets 
        #To distinguish items that user doesn't own any there is a big jum in color from 0 to 1 number of items 
        R = round(144 * (quantity/float(top_amount)))  #144 + 60 for jump + 51 witch is the based = 255 
        if quantity !=0 : R += 60 # this is the jump
        c = "\033[38;2;{};{};100m".format(255 - R, 51 + R) #Determines the color, might not work on windows terminal... 

        report = c + "[" + str(quantity) + "]" + item.name + "\033[0m " 

        print(report)

    # Call to get point value, didn't find anywhere market value for points so it has to looks at all the points 
    # that are soled atm and take price form the lowest as the market value
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
    #Just a lot of text to print showing variables 

    print("\nOne set:")
    print("     Cost to complete:"+Fore.GREEN+" ${:,}".format(one_set_cost_complete))
    print("     Worth on market: ${:,}".format(one_set_cost_market))
    print("     Worth in museum: ${:,}".format(one_set_cost_museum))
    difference = one_set_cost_museum - one_set_cost_market
    if difference >= 0: print("     Difference:"+ Fore.GREEN + " ${:,}".format(difference))
    else: print("     Difference:"+ Fore.RED + " ${:,}".format(difference))


    print("\nMax set [{}]:".format(top_amount))
    print("     Cost to complete:"+ Fore.GREEN +" ${:,}".format(max_set_cost_complete))
    print("     Worth on market: ${:,}".format(max_set_cost_market))
    print("     Worth in museum: ${:,}".format(max_set_cost_museum))
    difference = max_set_cost_museum - max_set_cost_market
    if difference >= 0: print("     Difference:"+ Fore.GREEN + " ${:,}".format(difference))
    else: print("     Difference:"+ Fore.RED + " ${:,}".format(difference))

    #Current sett is only shown when you can exchange at least one set at the museum 

    if min_amount != 0:
        print("\nCurrent set [{}] :".format(min_amount))
        print("     Worth on market: ${:,}".format(current_set_cost_market))
        print("     Worth in museum: ${:,}".format(current_set_cost_museum))
        difference = current_set_cost_museum - current_set_cost_market
        if difference >= 0: print("     Difference:"+ Fore.GREEN + " ${:,}".format(difference))
        else: print("     Difference:"+ Fore.RED + " ${:,}".format(difference))

        print("\n https://www.torn.com/museum.php \n")
    
    # updating the table every 30 second

    # one update makes total of 3 calls since you get two updates per minute this program takes
    # 6 API calls from the 100 available every minute (that's alright). 
    time.sleep(30) 
