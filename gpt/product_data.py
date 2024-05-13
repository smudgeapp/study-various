import json
import os
import time
import html2text



ht = html2text.HTML2Text()

product_file = 'E:\Projects\ebay_auto/aliex_item_data.json'

items = []

with open(product_file, 'r') as f:
    items = json.load(f)

print(len(items))

##for i in items:
##    desc = i['description']
##    print(desc)
##    text = html2text.html2text(desc)
##    text = text.encode('utf-8')
##    text = text.decode('utf-8')
##    print(text)
##    break
