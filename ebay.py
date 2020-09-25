#!/usr/bin/env python
import gevent.monkey
gevent.monkey.patch_all()
import faster_than_requests as requests
import time
import grequests
from fast_soup import FastSoup
from multiprocessing import Process, Queue
import multiprocessing
    
def main(kws):    
    def main(kws,ipg,pgn):
        #start_time1 = time.time()
        page = requests.get2str(f"https://www.ebay.com/sch/i.html?_nkw={kws}&_ipg={ipg}&_pgn={pgn}")
    
        soup = FastSoup(page) 
        a = soup.find_all('a', class_='s-item__link')
        links = [l.get("href") for l in a] 
        print(len(links))
        
        reqs = (grequests.get(link) for link in links)
        pages = grequests.map(reqs)

        n = 0
        itms = {}
        for p in pages:

            item_l = links[n].split("/")
            item = item_l[item_l.index("itm")+1]
                
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
            n += 1 #check needed: does n+1 skip when excpetion pass?
            
        Q.put(itms)
        #print("--- %s seconds ---" % (time.time() - start_time1))
    
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
    
    Q = Queue()
    processes = []
    for pgn in range(10):
        p = multiprocessing.Process(target = main,args = (kws, 25, pgn+1))
        p.start()
        processes.append(p)

    items = {}
    for process in processes:
        process.join()
        items.update(Q.get())
        
    sort_items = sorted(items.items(), key=lambda x: x[1])
    #for i in sort_items:
        #print(i[0],f"\n{i[1]}", "\n")
        
    return items


