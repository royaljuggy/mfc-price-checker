import requests
from bs4 import BeautifulSoup
from yen_parser import parse_yen
from currency_converter import CurrencyConverter

import sys

# TODO: error checking if user doesn't have public profile
def main():
    # constants
    if (len(sys.argv) == 2): # first arg is program name
        username = sys.argv[1]
    else:
        username = "SkillSwap"
    
    # global variables 
    # TODO - is there a better syntax?
    global ROOT_URL

    ROOT_URL = "https://myfigurecollection.net"

    # statistic variables
    no_price_counter = 0
    cost_in_yen = 0
    num_items = 0
    num_prizes = 0

    # scrape user info page
    URL = ROOT_URL + "/profile/" + username
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    
    # click into full figure collection view
    URL = ROOT_URL + soup.findAll("ul", class_="subtab")[1].find("a").get("href")
    subtabs = soup.findAll("ul", class_="subtab")
    for subtab in subtabs:
        
        cursoup = subtab.find("a")
        if "Owned" not in cursoup.text:
            continue
        URL = ROOT_URL + cursoup.get("href")
        page = requests.get(URL)
        newsoup = BeautifulSoup(page.content, "html.parser")
        
        # scrape a page full of figure prices
        while True:
            stats = scrape_page(newsoup)
            no_price_counter += stats[0]
            cost_in_yen += stats[1]
            num_items += stats[2]
            num_prizes += stats[3]

            # get next page of figures
            URL = soup.find("a", class_="nav-next")
            if URL == None:
                break
            else:
                URL = URL.get("href")
            page = requests.get(URL)
            soup = BeautifulSoup(page.content, "html.parser")


    # Print statistics, convert from yen to cad
    c = CurrencyConverter()

    print("\n=== Total cost: ===")
    print("\tin YEN: " + str(cost_in_yen))

    # convert from JPY to CAD and round to 2 decimal places
    print("\tin CAD: " + str(round(c.convert(cost_in_yen, 'JPY', 'CAD'), 2)) + "\n")

    print("=== Some statistics ===")
    print("\tFigures with no price available: " + str(no_price_counter))
    print("\tNumber of items: " + str(num_items) + "\n")
    #print("\tNumber of prize figures: " + str(num_items) + "\n")

# === end main

# Scrape a page worth of figure prices
def scrape_page(page_soup):

    no_price_counter = 0
    cost_in_yen = 0
    num_items = 0
    num_prizes = 0

    # find first container for figure icons
    figure_icons = page_soup.find("div", class_="item-icons")

    for figure_icon in figure_icons:
        num_items += 1
        URL = ROOT_URL + figure_icon.find("a", class_="tbx-tooltip").get("href")
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, "html.parser")

        # scrape price for current figure (default price type = YEN)
        try:
            price = soup.find("span", class_="item-price").text
            cost_in_yen += parse_yen(price)
        except:
            no_price_counter += 1
    return [no_price_counter, cost_in_yen, num_items, num_prizes]
# end page scrape

# main func runner
if __name__ == "__main__":
    main()