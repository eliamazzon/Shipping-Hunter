#!/usr/bin/env python
import gevent.monkey
gevent.monkey.patch_all()
import requests
import time
import playsound
import grequests
from bs4 import BeautifulSoup
from selectolax.parser import HTMLParser

def range_adapter(rango1): #let's find a better way'

        calendar = {
            'Jan.' : 1,
            'Feb.' : 2,
            'Mar.' : 3,
            'Apr.' : 4,
            'May.' : 5,
            'Jun.' : 6,
            'Jul.' : 7,
            'Aug.' : 8,
            'Sep.' : 9, 
            'Oct.' : 10,
            'Nov.' : 11,
            'Dec.' : 12
        }
        r1_0 = calendar[rango1[0]]
        r1_2 = calendar[rango1[2]]
        
        return r1_0, r1_2


kws = input("type keywords here: ")
start_time = time.time()
link = f"https://www.ebay.com/sch/i.html?_nkw={kws}&_ipg=25"  
page = requests.get(link) #1.5

soup = BeautifulSoup(page.text,"lxml") 
a = soup.find_all('a', class_='s-item__link')

links = [] #just the first page, iterate with the others

for l in a:
    l.find(href=True)
    links.append(l.get("href"))

print(len(links))
reqs = (grequests.get(link) for link in links)
try:
    page = grequests.imap(reqs, grequests.Pool(10))
except Exception as e: 
    print(e)
    pass    

n = 0
items = {}

for p in page:
   
    l = links[n]
    item_l = l.split("/")
    item_index = (item_l.index("itm") + 1)
    item = item_l[item_index]
        
    soup = BeautifulSoup(p.text, 'lxml') 
    span = soup.find_all('span', class_='vi-acc-del-range')
    try:
        b = span[0].find("b")  
        delivery = (b.get_text()).split(" ")
        rango1 = [delivery[1],delivery[2],delivery[5],delivery[6]]
        rng = range_adapter(rango1)
        rango1[0] = rng[0]
        rango1[2] = rng[1]
        items[item] = rango1 #item_name & shipping_date added to the dictionary
    except Exception as e: 
        print(e)
        pass
    
    n += 1

print(len(items))
sort_items = sorted(items.items(), key=lambda x: x[1])

for i in sort_items:
    print(i[0],f"\n{i[1]}", "\n")
    # add product link & try to filter results to make them relevant

playsound.playsound('4.mp3', True)
print("--- %s seconds ---" % (time.time() - start_time))


