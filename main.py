#!/usr/bin/env python
import gevent.monkey
gevent.monkey.patch_all()
import faster_than_requests as requests
import time
import playsound
import grequests
from fast_soup import FastSoup
from selectolax.parser import HTMLParser
from multiprocessing import Process, Queue
import multiprocessing

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

def main(kws,ipg,pgn):
    #start_time1 = time.time()
    page = requests.get2str(f"https://www.ebay.com/sch/i.html?_nkw={kws}&_ipg={ipg}&_pgn={pgn}")
    
    soup = FastSoup(page) 
    a = soup.find_all('a', class_='s-item__link')

    links = [] 

    for l in a:
        l.get("href")
        links.append(l.get("href"))

    print(len(links))
    reqs = (grequests.get(link) for link in links)
    page = grequests.map(reqs)

    n = 0
    itms = {}

    for p in page:
        
        l = links[n]
        item_l = l.split("/")
        item_index = (item_l.index("itm") + 1)
        item = item_l[item_index]
            
        soup = FastSoup(p.text) 
        span = soup.find('span', class_='vi-acc-del-range')
        try:
            b = span.find("b")  
            delivery = (b.get_text()).split(" ")
            rango1 = [delivery[1],delivery[2],delivery[5],delivery[6]]
            rng = range_adapter(rango1)
            rango1[0] = rng[0]
            rango1[2] = rng[1]
            itms[item] = rango1 #item_name & shipping_date 
            #added to the dictionary
        except Exception as e: 
            print(e)
            pass
        
        n += 1
    
    Q.put(itms)
    #print("--- %s seconds ---" % (time.time() - start_time1))

    
Q = Queue()


kws = "iphone"#input("type keywords here: ")
start_time = time.time()
ipg = 25
pgs = 10

processes = []

for pgn in range(pgs):
    p = multiprocessing.Process(target = main,args = (kws, ipg, pgn+1))
    p.start()
    processes.append(p)

items = {}
for process in processes:
    process.join()
    items.update(Q.get())
    
    

sort_items = sorted(items.items(), key=lambda x: x[1])

#for i in sort_items:
    #print(i[0],f"\n{i[1]}", "\n")
    # add product link & try to filter results to make them relevant
print(len(items))
#playsound.playsound('4.mp3', True)
print("--- %s seconds ---" % (time.time() - start_time))


