# -*- coding: utf-8-*-
import json
import threading

import time
import datetime

from grab import Grab

class Main():
    list_items = []
    list_threads = []


    def __init__(self):

        self.set_collection_items()
        grouped_items = self.group_list_items(1)

        for group_items in grouped_items:
            self.list_threads.append(threading.Thread(target=self.write_price, kwargs={"group_items": group_items}))

        for thread in self.list_threads:
            thread.start()

        for thread in self.list_threads:
            thread.join()

    def set_collection_items(self):
        with open("items/items.txt") as f:
            for line in f.readlines():
                line = line.rstrip()
                item = line.split(" --- ")
                self.list_items.append(item)

    def group_list_items(self, n):
        """ Группировка items по n элементов """
        return [self.list_items[i:i + n] for i in range(0, len(self.list_items), n)]

    def write_price(self, group_items):
        g = Grab()
        url = "http://steamcommunity.com/market/itemordershistogram?country=RU&language=russian&currency=5&two_factor=0&"

        while True:

            for item in group_items:
                print item[0].decode('utf-8')
                time_now = datetime.datetime.now()
                time_now = time_now.strftime('%d %b %Y %H:%M:%S')
                try:
                    g.go(url+item[1])
                    responce = json.loads(g.response.body)

                    responce["time_now"] = time_now
                    del(responce["price_suffix"])
                    del(responce["sell_order_table"])
                    del(responce["sell_order_summary"])
                    del(responce["buy_order_table"])
                    del(responce["buy_order_summary"])
                    del(responce["graph_max_y"])
                    del(responce["graph_min_x"])
                    del(responce["graph_max_x"])
                    del(responce["price_prefix"])

                    for point in responce['sell_order_graph']:
                        del(point[2])
                    for point in responce['buy_order_graph']:
                        del(point[2])

                    responce['sell_order_graph'] = responce['sell_order_graph'][:10]
                    responce['buy_order_graph'] = responce['buy_order_graph'][:10]
                    for i in reversed(xrange(1, len(responce['sell_order_graph']))):
                        a = int(responce['buy_order_graph'][i][1])
                        b = int(responce['buy_order_graph'][i-1][1])
                        responce['buy_order_graph'][i][1] = a-b

                    for i in reversed(xrange(1, len(responce['sell_order_graph']))):
                        a = int(responce['sell_order_graph'][i][1])
                        b = int(responce['sell_order_graph'][i-1][1])
                        responce['sell_order_graph'][i][1] = a-b
                except:
                    print 'SOMETHING WRONG!'
                    continue

                file_name = 'items/3_item '+item[0]+'.txt'
                file_name = file_name.decode('utf-8')
                with open(file_name, 'a') as f:
                    f.write(json.dumps(responce)+'\n')
                f.close()
            time.sleep(60)

if __name__ == "__main__":
    Main()
