# Apple Stock or Apple Product?

A simple exploration into the world of missed opportunities.


## Installation

    pip install -r requirements.txt

## Creating the Dataset 

    python scrape_everymac.py
    python ipod_or_stock.py

The output will be `apple-specs-with-current.json` which includes the original prices for each item as well as how many shares that item was worth on release day.

## Thanks

Big thanks to <http://www.everymac.com> for the data. Also, if you ever need to parse HTML in Python, BeautifulSoup is amazing. 

apple-specs.json contains detailed specs for almost every Apple product released in the last thirteen years. I hope someone finds it useful. 
