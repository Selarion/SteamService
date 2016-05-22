# -*- coding: utf-8-*-
import Queue


class TradeWorkerController(object):
    def __init__(self, trade_worker):
        self.trade_worker = trade_worker
        self.input_queue = Queue.Queue()
        self.output_queue_searcher = None
        self.output_queue_executor = None

    def start_routing(self):
        while True:
            try:
                new_incoming_task = self.input_queue.get()
                self.route_task(new_incoming_task)
            except Queue.Empty:
                pass

    def route_task(self, new_incoming_task):
        print new_incoming_task
                
    def get_input_queue(self):
        return self.input_queue

    def set_output_queue_searcher(self, output_queue):
        self.output_queue_searcher = output_queue

    def get_output_queue_searcher(self):
        return self.output_queue_searcher

    def set_output_queue_executor(self, output_queue):
        self.output_queue_executor = output_queue

    def get_output_queue_executor(self):
        return self.output_queue_executor
