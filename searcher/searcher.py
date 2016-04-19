# -*- coding: utf-8-*-
import json
import random
import threading
import time

from controllers.searcher_controller import SearcherController
from grab import Grab


class Searcher:
    def __init__(self):
        self.controller = SearcherController(self)

    def start(self, output_queue):
        print 'searcher thread is start'
        self.controller.set_output_queue(output_queue)
        self.controller.start_routing()

    def check_trade_profit(self, new_task, output_queue):
        item_class = new_task.get_item_class()
        th = threading.Thread(target=self.get_actual_price,
                              name='Thread item_nameid '+item_class.get_item_nameid(),
                              kwargs={'item_class': item_class,
                                      'output_queue': output_queue})
        th.setDaemon(True)
        th.start()

    def get_actual_price(self, item_class, output_queue):
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
            item_class.set_highest_buy_order(highest_buy_order)
        except Exception as inst:
            print type(inst)  # the exception instance
            print inst
            return
        if item_class.get_profit() > 0:
            output_queue.put(item_class)

    def get_input_queue(self):
        return self.controller.get_input_queue()
