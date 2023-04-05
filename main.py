from bs4 import BeautifulSoup
import requests 
import numpy as np
import csv
from datetime import datetime
import time
import re

LINK = "https://listado.mercadolibre.com.ar/computacion/monitores-accesorios/monitores/samsung/nuevo/monitor-27_OrderId_PRICE_NoIndex_True#applied_filter_id%3DBRAND%26applied_filter_name%3DMarca%26applied_filter_order%3D3%26applied_value_id%3D206%26applied_value_name%3DSamsung%26applied_value_order%3D24%26applied_value_results%3D207%26is_custom%3Dfalse"

def get_prices_by_link(link):
    # get source
    r = requests.get(link)
    # parse source 
    page_parse = BeautifulSoup(r.text, "html.parser")
    # find all list items from results 
    search_results = page_parse.find_all("li",{"class":"ui-search-layout__item"}, limit=10)

    items = []

    # Extract value, name, and link of the items
    for item in search_results:
        item_name = item.find("a",{"ui-search-item__group__element shops__items-group-details ui-search-link"}).text
        item_value = item.find("span",{"class":"price-tag-text-sr-only"}).text
        item_value = re.findall(r'\d+', item_value)
        item_value = float(item_value[0])
        item_link = item.find("a",{"ui-search-item__group__element shops__items-group-details ui-search-link"}).get("href")
        # print values
        item = [item_name, item_value, item_link]
        items.append(item)
    return items

def save_to_file(prices):
    for prices in prices[1:10]:
        with open("prices.csv", "a", newline="") as csvfile:
            fields = [datetime.today().strftime("%D-%B-%Y"), prices[0], prices[1], prices[2]]
            writer = csv.writer(csvfile)
            writer.writerow(fields)
        
if __name__ == "__main__":
    while True:
        items = get_prices_by_link(LINK)
        save_to_file(items)
        # Execute every 8 hours   
        time_wait = 8
        print(f"Waiting {time_wait} minutes...")
        time.sleep(time_wait * 3600)