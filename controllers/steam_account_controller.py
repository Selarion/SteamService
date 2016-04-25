# -*- coding: utf-8-*-
import Queue

class SteamAccountController():
    def __init__(self, steam_account):
        self.steam_account = steam_account
        self.input_queue = Queue.Queue()
        self.output_queue = None

    def start_route(self):
        while True:
            try:
                new_task_from_executor = self.input_queue.get()
                print(new_task_from_executor)
            except StandardError:
                pass

    def get_input_queue(self):
        return self.input_queue

    def get_output_queue(self):
        return self.output_queue

    def set_output_queue(self, output_queue):
        self.output_queue = output_queue