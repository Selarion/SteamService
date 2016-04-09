# -*- coding: utf-8-*-
import Queue
import json
import random
import threading

from grab import Grab
import time


class CheckerPrices:
    def __init__(self):
        self.input_queue = Queue.Queue()
        self.output_queue = Queue.Queue()

    def start(self):
        print 'snatcher thread is start'
        self.start_main_event_loop()

    def start_main_event_loop(self):
        while True:
            item_class = self.input_queue.get()
            th = threading.Thread(target=self.get_actual_price,
                                  name='Thread item_nameid '+item_class.get_item_nameid(),
                                  kwargs={'item_class': item_class})
            th.setDaemon(True)
            th.start()

    def get_actual_price(self, item_class):
        try:
            url_price = "steamcommunity.com/market/itemordershistogram?country=RU&language=russian&currency=5&" \
                        "item_nameid=%s&two_factor=0" % item_class.get_item_nameid()
            g = Grab(log_file='log.html')
            g.setup(url=url_price)
            time.sleep(random.uniform(0, 2))
            g.request()
            responce = json.loads(g.response.body)
            lowest_sell_price = float(responce['lowest_sell_order'])/100
            highest_buy_order = float(responce['highest_buy_order'])/100
            item_class.set_lowest_sell_price(lowest_sell_price)
            item_class.set_highest_buy_order(highest_buy_order, refresh_profit_flag=True)
        except Exception as inst:
            print type(inst)     # the exception instance
            print inst
            return
        if item_class.get_profit() > 0:
            self.output_queue.put(item_class)

    def get_input_queue(self):
        return self.input_queue

    def get_output_queue(self):
        return self.output_queue