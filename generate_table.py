import json
import xml.etree.ElementTree as etree

table = etree.Element("table", attrib={
    "id": "apple",
    "class": "tablesorter",
    "cellspacing": "1",
    "cellpadding": "0",
    })

thead = etree.SubElement(table, "thead")
tbody = etree.SubElement(table, "tbody")
tr = etree.SubElement(thead, "tr")

for heading in ["Product", "Release Date", "Original Price", "Stock Value Today"]:
    th = etree.SubElement(tr, "th")
    th.text = heading

for product in json.load(open("apple-specs-with-current.json")):
    row = etree.SubElement(tbody, "tr")

    value = 0

    data = [
        product["name"],
        product["introduction-date"].split("T")[0],
        "$" + unicode(product["original-price"]),
        "${:d}".format(int(product["stock-shares"] * 599.55)),
    ]

    for field in data:
        td = etree.SubElement(row, "td")
        td.text = field

print etree.tostring(table)
