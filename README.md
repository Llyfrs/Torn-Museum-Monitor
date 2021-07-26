# Torn-Museum-Monitor
Python script for monitoring amount of items corresponding to certain museum set.

## Installing

For running this python script you will need colorama and request packages. You can install them using commands shown bellow. 

```
pip install colorama
pip install request
```
alternatively you can use `envpip install` if you know what it is. 

## Usage 

First you need to edit the code and insert your own API, its the first variable. If you don't edit the code you will be asked for the API key at the start of the application this will not save your API anywhere and will be asked every time you run the program.
You can now run the script it will ask you to choose between plushie set and flower set. Choose one by pressing 1 or 2 and enter.
Now your have a loop running updating every 30 second your inventory.

## Displayed information

First you can see all items for selected set, base on the amount you own the text will be colored from red to green, where red means you don’t own any off the items and completely green is the item you have most of. You can also see the exact amount in []. 

Second part of displayed information shows possible profits by buying at market value and getting points for them in museum. 

- One set shows values for only one set of items.

- Max set show values for selling number off sets corresponding to the item you have most (most green item).

- Current set is only visible when you can exchange at leas one set at the museum.



All profits are theoretical if you stick to buying always under market price and  wait for points to rise in value you can make more money and vise versa. Flying makes approximately 11K a minute that means one would need to complete at leas one set per minute to compete with flying profits. 
