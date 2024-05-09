import requests
from bs4 import BeautifulSoup
from currency_converter import CurrencyConverter
import re
import sys
from time import sleep
from tqdm import tqdm

# TODO: error checking if user doesn't have public profile
def main():
    # constants
    if (len(sys.argv) == 2): # first arg is program name
        username = sys.argv[1]
    else:
        print("Please enter a user name!")
        return
    
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
    URL = ROOT_URL + "/profile/" + username + "/collection/"
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    
    # click into full figure collection view
    subtabs = soup.findAll("a", class_="nav-page")
    for subtab in subtabs:
        
        URL = subtab.get("href").replace("amp;", "")
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

# === end main

# Scrape a page worth of figure prices
def scrape_page(page_soup):

    no_price_counter = 0
    cost_in_yen = 0
    num_items = 0
    num_prizes = 0

    figures = page_soup.findAll("span", class_="item-icon")
    print("Scraping a page...")
    for i in tqdm(range(len(figures))):
        figure = figures[i]
        num_items += 1
        URL = ROOT_URL + figure.find("a").get("href")
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, "html.parser")

        # scrape price for current figure (default price type = YEN)
        try:
            # hacky!!
            price = int(re.findall("\d{1,3}(?:,\d{3})*(?= JPY)", soup.find("a", {'title' : 'convert into USD'}).find_parent("div").getText())[0].replace(',', ''))
            cost_in_yen += price
        except:
            no_price_counter += 1

        # Sleep to avoid rate limit.
        sleep(1)
    print("Page data")
    print("Cost in yen: ", cost_in_yen)
    return [no_price_counter, cost_in_yen, num_items, num_prizes]
# end page scrape

# main func runner
if __name__ == "__main__":
    main()