# -*- coding: utf-8-*-
import json
import random
import threading
import Queue
import time

from grab import Grab

from database.basemodel import ItemClassList


def cheker_price(queue, item):
    while True:
        try:
            time.sleep(random.uniform(3, 5))
            url_price = "steamcommunity.com/market/itemordershistogram?country=RU&language=russian&currency=5&item_nameid=%s&two_factor=0" % item.item_nameid
            lof_file = item.name.replace(" | ", "")
            g = Grab(url=url_price, log_file=lof_file+'.html')
            g.request()
            responce = json.loads(g.response.body)
            lowest_sell_price = float(responce['lowest_sell_order'])
            highest_buy_order = float(responce['highest_buy_order'])
            profit = highest_buy_order/lowest_sell_price
            if profit < 0.85:
                queue.put(item.name + " -- "+ str(profit))
        except Exception as e:
            print e
            continue



def writer(queue):
    rnd = random.uniform(0, 2)
    print "--- " + str(rnd)
    time.sleep(rnd)
    if rnd > 1.5:
        queue.put(rnd)


def main():
    queue = Queue.Queue()

    i = 0
    for item in ItemClassList.select().where((ItemClassList.actual_price > 2) & (ItemClassList.actual_price < 10)):
        th = threading.Thread(name=item.name, target=cheker_price, args=[queue, item])
        th.setDaemon(True)
        th.start()
        i += 1

    t1 = time.time()
    while True:
        if (time.time() - t1) < 5:
            if queue.qsize() != 0:
                print queue.get()
                t1 = time.time()
        else:
            break

    raw_input('!!!!!')

    threading_pool = [None]*10
    queue = Queue.Queue()

    for i in range(len(threading_pool)):
        threading_pool[i] = threading.Thread(target=writer, args=[queue])

    for thread in threading_pool:
        thread.start()

    t1 = time.time()
    while True:
        if (time.time() - t1) < 600:
            if queue.qsize() != 0:
                print queue.get()
                t1 = time.time()
        else:
            break



if __name__ == '__main__':
    main()