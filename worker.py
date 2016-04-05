# -*- coding: utf-8-*-
import copy
import time

from database import database_methods as db
from executor.executor import Executor
from snatcher.snatcher import Snatcher

import threading, Queue


class Worker:
    def __init__(self):
        self.all_item_classes = list()
        self.in_buy_item_classes = list()
        self.in_sell_item_classes = list()
        self.in_check_item_classes = list()

        self.out_snatcher_queue = Queue.Queue()
        self.in_snatcher_queue = Queue.Queue()
        self.out_executor_queue = Queue.Queue()
        self.in_executor_queue = Queue.Queue()

        self.exeucotor = Executor()
        self.snatcher = Snatcher()

        self.snatcher_thread = threading.Thread(target=self.snatcher.test,
                                                name='SnatcherThread',
                                                kwargs={'input_queue': self.out_snatcher_queue,
                                                        'output_queue': self.in_snatcher_queue})
        self.executor_thread = threading.Thread(target=self.exeucotor.test,
                                                name='ExecutorThread',
                                                kwargs={'input_queue': self.out_executor_queue,
                                                        'output_queue': self.in_executor_queue})



        self.start()

    def start(self):
        self.snatcher_thread.start()
        self.executor_thread.start()

        self.all_item_classes = db.get_default_itemclass_list()
        self.in_buy_item_classes = self.all_item_classes[5:50]
        self.in_sell_item_classes = self.all_item_classes[50:]

        while True:
            self.refresh_in_check_item_classes()
            for item_class in self.all_item_classes:
                self.out_snatcher_queue.put(item_class.item_nameid)

            while not self.out_snatcher_queue.empty():
                print self.in_snatcher_queue.get()
            print '------'
            time.sleep(0.3)

    def refresh_in_check_item_classes(self):
        temporary_dict = self.all_item_classes
        for item_class in self.in_sell_item_classes:
            for item_class2 in temporary_dict:
                if item_class.name == item_class2.name:
                    temporary_dict.remove(item_class2)
        for item_class in self.in_buy_item_classes:
            for item_class2 in temporary_dict:
                if item_class.name == item_class2.name:
                    temporary_dict.remove(item_class2)
        self.in_check_item_classes = temporary_dict

if __name__ == '__main__':
    raw_input('test_branch')
    w = Worker()