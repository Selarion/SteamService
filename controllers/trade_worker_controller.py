# -*- coding: utf-8-*-
import Queue
import time


class TradeWorkerController():
    def __init__(self, trade_worker):
        self.trade_worker = trade_worker
        self.input_queue = Queue.Queue()

    def start_routing(self):
        while True:
            while True:
                try:
                    new_incoming_task = self.input_queue.get_nowait()
                    self.rout_task(new_incoming_task)
                except Queue.Empty:
                    break
            self.trade_worker.search_trade_value_item_classes()
            time.sleep(1)
            print '----'

    def rout_task(self, new_incoming_task):
        print new_incoming_task
                
    def get_input_queue(self):
        return self.input_queue