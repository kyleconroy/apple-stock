# This code was intended to run once (and only once) so I made no effort 
# to make it pretty
# Huge thanks to everymac for all the information

import urllib
import urllib2
from BeautifulSoup import BeautifulSoup
import re, htmlentitydefs
import urlparse
import os
import pprint
import json
import HTMLParser

def slugify(string):
    string = re.sub('\s+', '-', string)
    string = re.sub('[\._]', '-', string)
    string = re.sub('[^\w.-]', '', string)
    return string.strip('_.- ').lower()
    
def unescape(text):
    def fixup(m):
        text = m.group(0)
        if text[:2] == "&#":
            # character reference
            try:
                if text[:3] == "&#x":
                    return unichr(int(text[3:-1], 16))
                else:
                    return unichr(int(text[2:-1]))
            except ValueError:
                pass
        else:
            # named entity
            try:
                text = unichr(htmlentitydefs.name2codepoint[text[1:-1]])
            except KeyError:
                pass
        return text # leave as is
    return re.sub("&#?\w+;", fixup, text)
    
def parse_all_products():
    urls = [
        "http://www.everymac.com/systems/apple/powermac_g3/index-powermac-g3.html",
        "http://www.everymac.com/systems/apple/mac_server_g3/index-mac-server-g3.html",
        "http://www.everymac.com/systems/apple/powerbook_g3/index-powerbook-g3.html",
        "http://www.everymac.com/systems/apple/powermac_g4/index-powermac-g4.html",
        "http://www.everymac.com/systems/apple/mac_server_g4/index-mac-server-g4.html",
        "http://www.everymac.com/systems/apple/powerbook_g4/index-powerbook-g4.html",
        "http://www.everymac.com/systems/apple/powermac_g5/index-powermac-g5.html",
        "http://www.everymac.com/systems/apple/mac_pro/index-macpro.html",
        "http://www.everymac.com/systems/apple/xserve/index-xserve.html",
        "http://www.everymac.com/systems/apple/imac/index-imac.html",
        "http://www.everymac.com/systems/apple/emac/index-emac.html",
        "http://www.everymac.com/systems/apple/mac_mini/index-macmini.html",
        "http://www.everymac.com/systems/apple/ibook/index-ibook.html",
        "http://www.everymac.com/systems/apple/macbook/index-macbook.html",
        "http://www.everymac.com/systems/apple/macbook_pro/index-macbookpro.html",
        "http://www.everymac.com/systems/apple/macbook-air/index-macbook-air.html",
        "http://www.everymac.com/systems/apple/consumer_electronics/index-ipod.html",
        "http://www.everymac.com/systems/apple/apple-tv/index-appletv.html",
        "http://www.everymac.com/systems/apple/iphone/index-iphone-specs.html",
        "http://www.everymac.com/systems/apple/ipad/index-ipad-specs.html",
    ]
    
    data = []
    
    for url in urls:
        products = parse_products(url)
        data += products
        specs = open('apple-specs.json', 'w')
        json.dump(data, specs, sort_keys = True, indent = 4)
        specs.close()
        
def url_fetch(url):
    print url

    try:
        os.mkdir("cache")
    except OSError:
        pass

    _, filename = os.path.split(url)
    cached_file = os.path.join("cache", filename)

    if not os.path.exists(cached_file):
        urllib.urlretrieve(url, cached_file) 

    return open(cached_file)
 

def parse_products(url):
    products = []

    soup = BeautifulSoup(url_fetch(url))
    u = urlparse.urlparse(url)
    
    for span in soup.findAll('span', id="contentcenter_specs_externalnav_2"):
        a = span.a
        if a:
            path = os.path.join(os.path.dirname(u.path), a['href'])
            new_url = "%s://%s%s" % (u.scheme, u.netloc, path)
            product = parse_product(new_url)
            if product != None:
                products.append(product)
    
    return products

def parse_product(url):
    try:
        soup = BeautifulSoup(url_fetch(url))
    except HTMLParser.HTMLParseError:
        print "Could not parse %s" % url
        return None
        
    product = {}
    
    name = soup.find('h3')
    product["name"] = unescape(name.contents[0].replace("Specs", "").strip())
    
    # FIND ALL DETAILS
    for table in soup.findAll('table'):
        for tr in table.findAll('tr'):
            detail = ""
            value = ""
            for td in tr.findAll('td'):
                colon = False
            
                for i in td.contents:
                    if ":" in i:
                        colon = True
                        
                if len(td.contents) > 0:                    
                    if colon: 
                        detail = td.contents[-1:][0]
                    else:
                        value = td.contents[-1:][0]
                        if value == None or detail == None:
                            pass
                        elif "Details:" not in detail:
                            detail = detail.replace("Incl.", "included")
                            detail = detail.replace("Int.", "internal")
                            detail = detail.replace("Min.", "minimum")
                            detail = detail.replace("Max.", "maximum")
                            detail = detail.replace("Avg.", "average")
                            detail = detail.replace("Est.", "estimated")
                            key = slugify(unescape(detail))
                            value = str(value)
                            product[key] = unescape(value.replace("*",""))
                            
    return product

parse_all_products()

