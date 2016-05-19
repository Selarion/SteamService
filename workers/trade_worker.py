# -*- coding: utf-8-*-
import threading
import time

from executor.executor import Executor
from searcher.searcher import Searcher
from models.item_class import ItemClass
from models.tasks.check_profit_trade_task import CheckProfitTradeTask
from controllers.trade_worker_controller import TradeWorkerController


class TradeWorker:
    def __init__(self):
        # This block initializes the lists, that you need to trade.
        self.all_item_classes = set()
        self.in_buy_item_classes = set()
        self.in_sell_item_classes = set()
        self.in_freeze_item_classes = set()
        self.in_check_item_classes = set()

        self.controller = TradeWorkerController(self)
        self.executor = Executor()
        self.searcher = Searcher()

        # Initializes controller, executor and checker_items_prices threads.
        self.checker_price_thread = threading.Thread(target=self.searcher.start,
                                                     name='SearcherThread',
                                                     kwargs={'output_queue': self.controller.get_input_queue()})
        self.executor_thread = threading.Thread(target=self.executor.start,
                                                name='ExecutorThread',
                                                kwargs={'output_queue': self.controller.get_input_queue()})
        self.trade_worker_controller_thread = threading.Thread(target=self.controller.start_routing,
                                                               name='TradeWorkerControllerThread')

        self.__start()

    def __start(self):
        self.__load_start_data()
        self.__start_threads()
        self.__start_main_event_loop()

    def __load_start_data(self):
        # This is temporary block. It's necessary before checker and executor was finale finished.
        self.all_item_classes = set(ItemClass.get_default_itemclass_list()[:200])
        self.in_buy_item_classes = set(list(self.all_item_classes)[5:50])
        self.in_sell_item_classes = set(list(self.all_item_classes)[51:100])
        self.refresh_in_check_item_classes()

        self.controller.set_output_queue_searcher(self.searcher.get_input_queue())
        self.controller.set_output_queue_executor(self.executor.get_input_queue())

    def __start_threads(self):
        # Start threads.
        self.trade_worker_controller_thread.start()
        # self.checker_price_thread.start()
        self.executor_thread.start()

    def __start_main_event_loop(self):
        while True:
            print 'Generate new loop!'
            # self.search_trade_value_item_classes()
            self.controller.output_queue_executor.put(1)
            time.sleep(10)

    def search_trade_value_item_classes(self):
        for item_class in self.in_check_item_classes:
            task = CheckProfitTradeTask(item_class)
            self.controller.get_output_queue_searcher().put(task)

    def refresh_in_check_item_classes(self):
        self.in_check_item_classes = self.all_item_classes - self.in_buy_item_classes - self.in_sell_item_classes

if __name__ == '__main__':
    w = TradeWorker()
