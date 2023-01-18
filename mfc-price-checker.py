import requests
from bs4 import BeautifulSoup
from yen_parser import parse_yen
from currency_converter import CurrencyConverter

username = "SkillSwap"
ROOT_URL = "https://myfigurecollection.net"
# scrape user info page
URL = ROOT_URL + "/profile/" + username
page = requests.get(URL)

soup = BeautifulSoup(page.content, "html.parser")

# find first container for figure icons
figure_icons = soup.find("div", class_="item-icons")

no_price_counter = 0
cost_in_yen = 0
# c = CurrencyConverter()

for figure_icon in figure_icons:
    # print(figure_icon, end="\n"*2)
    URL = ROOT_URL + figure_icon.find("a", class_="item-root-0").get("href")
    # print(URL)
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

print("The total cost:");
print("\tin YEN: " + str(cost_in_yen))

# convert from JPY to CAD and round to 2 decimal places
print("\tin CAD: " + str(round(c.convert(cost_in_yen, 'JPY', 'CAD'), 2)))
print("Number of figures/items with no price available: " + str(no_price_counter))
