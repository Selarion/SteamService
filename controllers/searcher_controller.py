# -*- coding: utf-8-*-
import Queue

from models.tasks.check_profit_trade_task import CheckProfitTradeTask


class SearcherController:
    def __init__(self, searcher):
        self.searcher = searcher
        self.input_queue = Queue.Queue()
        self.output_queue = None

    def start_routing(self):
        while True:
            try:
                new_incoming_task = self.input_queue.get()
                self.route_task(new_incoming_task)
            except Queue.Empty:
                pass

    def route_task(self, new_task):
        if isinstance(new_task, CheckProfitTradeTask):
            self.searcher.check_trade_profit(new_task, self.output_queue)
        else:
            print 'DOMETHING WRONG'

    def get_input_queue(self):
        return self.input_queue

    def get_output_queue(self):
        return self.output_queue

    def set_output_queue(self, output_queue):
        self.output_queue = output_queue