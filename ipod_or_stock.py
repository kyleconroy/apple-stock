import csv
import re
import json
from datetime import datetime
from datetime import date
from datetime import timedelta

def get_stock_prices(csv_file):
    current_price = 599.55 # March 30, 2012
    prices = {}
    stockReader = csv.reader(open(csv_file), delimiter=',')
    
    stockReader.next() # Throw away column headings
    
    for i, row in enumerate(stockReader):
        if i == 0:
            current_price = row[6]
        date_object = datetime.strptime(row[0], '%Y-%m-%d')
        prices[date_object] = row[6]
        
    return (prices, float(current_price))
    
def get_products(json_file):
    products = json.load(open(json_file))
    
    for product in products:
        try:
            price =  product["original-price"]
        except KeyError:
            price =  product["original-price-us"]

        match = re.match(r"US\$(\d+).*",price)
        if match:
            product["original-price"] = float(match.groups()[0])
        else:
            product["original-price"] = 0.0
            
        date = product["introduction-date"]
        date_object = datetime.strptime(date, '%B %d, %Y ')
        product["introduction-date"] = date_object
            
    return products
    
def find_price(prices, date):
    for i in range(8):
        try:
            return float(prices[date])
        except KeyError:
            date = date + timedelta(days=1)
    return False
        
    
def calculate_lost_money(prices, products, current_price):
    first_split = datetime(2000,1,21)
    second_split = datetime(2005,2,28)
    
    for product in products:
        
        price = float(product["original-price"])
        
        if price > 0:
            intro_date = product["introduction-date"]
            old_stock_price = find_price(prices, intro_date)
            shares = price / old_stock_price
            product["stock-shares"] = shares
        else:
            shares = 0
            product["stock-shares"] = shares

        product["introduction-date"] = product["introduction-date"].isoformat()
    
    return products


if __name__ == '__main__':
    stock_csv = "apple_stock_data.csv"
    product_csv = "apple_products_data.csv"
    
    prices, current_price = get_stock_prices(stock_csv)
    products = get_products('apple-specs.json')
    products = calculate_lost_money(prices, products, current_price)
    
    specs = open('apple-specs-with-current.json', 'w')
    json.dump(products, specs, sort_keys = True, indent = 4)
    specs.close()
    
