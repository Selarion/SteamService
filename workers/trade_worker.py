# -*- coding: utf-8-*-
import time
import threading
import Queue
import datetime

from models.database import database_methods as db
from executor.executor import Executor
from searcher.checkerprices import CheckerPrices


class TradeWorker:
    def __init__(self):
        # This block initializes the lists, that you need to trade.
        self.all_item_classes = set()
        self.in_buy_item_classes = set()
        self.in_sell_item_classes = set()
        self.in_check_item_classes = set()

        # Initializes executor and checker_item_prices.
        self.executor = Executor()
        self.checker_prices = CheckerPrices()

        # Initializes executor and checker_items_prices threads.
        self.checker_price_thread = threading.Thread(target=self.checker_prices.start,
                                                     name='CheckerPriceThread')
        self.executor_thread = threading.Thread(target=self.executor.start_main_loop,
                                                name='ExecutorThread')
        # Start main_event_loop.
        self.__load_start_data()
        self.__start_threads()
        self.start_main_event_loop()

    def __load_start_data(self):
        # This is temporary block. It's necessary before checker and executor was finale finished.
        self.all_item_classes = set(db.get_default_itemclass_list()[:200])
        self.in_buy_item_classes = set(list(self.all_item_classes)[5:50])
        self.in_sell_item_classes = set(list(self.all_item_classes)[51:100])

    def __start_threads(self):
        # Start threads.
        self.checker_price_thread.start()
        self.executor_thread.start()

    def start_main_event_loop(self):
        """
        This is main_event_loop is composed of next steps:
        Step 1 - work with input queues ("check new data" as example).
        Stem 2 - some logic (maybe).
        step 3 - work with output queues ("create task" as example).
        """
        # This is main_loop_event.
        while True:
            print datetime.datetime.strftime(datetime.datetime.now(), "%H:%M:%S")
            # Begin step 1:
            while True:
                try:
                    new_value_to_trade_item_class = self.checker_prices.get_output_queue().get_nowait()
                    """
                    print new_value_to_trade_item_class.get_name()
                    print new_value_to_trade_item_class.get_market_link()
                    print new_value_to_trade_item_class.get_lowest_sell_price()
                    print new_value_to_trade_item_class.get_highest_buy_order()
                    print new_value_to_trade_item_class.get_profit()
                    """
                except Queue.Empty:
                    print 'self.in_checker_items_prices_queue is empty'
                    break
            while True:
                try:
                    new_task_from_executor = self.executor.get_output_queue().get_nowait()
                except Queue.Empty:
                    print 'self.in_executor_queue is empty'
                    break
            # Begin step 2:
            # As a result of this operation we get actual "in_check_item_list".
            self.refresh_in_check_item_classes()

            # Begin step 3:
            # SEND item_nameid FROM item_class list TO "checker_items_prices" thread THROUGH queue.
            # When "checker_items_prices" thread get item_nameid from this queue, it will create
            # child thread for item_nameid and get price from http://steamcommunity.com.
            for item_class in self.in_check_item_classes:
                self.checker_prices.get_input_queue().put(item_class)
            print '------'
            time.sleep(5)

    def refresh_in_check_item_classes(self):
        self.in_check_item_classes = self.all_item_classes - self.in_buy_item_classes - self.in_sell_item_classes

if __name__ == '__main__':
    w = TradeWorker()