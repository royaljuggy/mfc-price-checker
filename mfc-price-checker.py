import requests
from bs4 import BeautifulSoup
from yen_parser import parse_yen
from currency_converter import CurrencyConverter

import sys
# constants
if (len(sys.argv) == 2): # first arg is program name
    username = sys.argv[1]
else:
    username = "SkillSwap"

ROOT_URL = "https://myfigurecollection.net"

# variables
no_price_counter = 0
cost_in_yen = 0
num_items = 0
num_prizes = 0

# scrape user info page
# TODO - the following only shows the first 40 figures for an individual! Fix this!
URL = ROOT_URL + "/profile/" + username
page = requests.get(URL)

soup = BeautifulSoup(page.content, "html.parser")

# find first container for figure icons
figure_icons = soup.find("div", class_="item-icons")

for figure_icon in figure_icons:
    num_items += 1
    URL = ROOT_URL + figure_icon.find("a", class_="item-root-0").get("href")
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")

    # scrape price for current figure (default price type = YEN)
    
    try:
        price = soup.find("span", class_="item-price").text
        
        # print(parse_yen(price))
        cost_in_yen += parse_yen(price)
    except:
        no_price_counter += 1

c = CurrencyConverter()

print("\n=== Total cost: ===");
print("\tin YEN: " + str(cost_in_yen))

# convert from JPY to CAD and round to 2 decimal places
print("\tin CAD: " + str(round(c.convert(cost_in_yen, 'JPY', 'CAD'), 2)) + "\n")

print("=== Some statistics ===")
print("\tFigures with no price available: " + str(no_price_counter))
print("\tNumber of items: " + str(num_items) + "\n")
#print("\tNumber of prize figures: " + str(num_items) + "\n")