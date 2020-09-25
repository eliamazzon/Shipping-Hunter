#!/usr/bin/env python
import time
import ebay
start_time = time.time()

items = {}
items.update(ebay.main("iphone"))
print(len(items))

print("--- %s seconds ---" % (time.time() - start_time))
