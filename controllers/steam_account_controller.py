# -*- coding: utf-8-*-
import Queue

from models.messages.request_trade_item import RequestTradeItem
from models.tasks.task_trade_item import TaskTradeItem


class SteamAccountController(object):
    def __init__(self, steam_account_task_pool):
        self.steam_account_task_pool = steam_account_task_pool
        self.input_queue = Queue.Queue()
        self.output_queue = None

    def start_route(self):
        while True:
            try:
                new_message_from_executor = self.input_queue.get()
                if isinstance(new_message_from_executor, RequestTradeItem):
                    new_task = TaskTradeItem(new_message_from_executor.get_item_class())
                    self.steam_account_task_pool.append(new_task)
                    print "sucsess"
            except StandardError:
                pass

    def get_input_queue(self):
        return self.input_queue

    def get_output_queue(self):
        return self.output_queue

    def set_output_queue(self, output_queue):
        self.output_queue = output_queue
