# -*- coding: utf-8-*-
import Queue
from grab import Grab


class SteamAccount:
    def __init__(self, login_steam, pass_steam, code_link):
        self.login_steam = login_steam
        self.pass_steam = pass_steam
        self.code_link = code_link

        self.input_queue = Queue.Queue()
        self.output_queue = Queue.Queue()

    def start_waiting_new_task(self):
        while True:
            try:
                new_task_from_executor = self.input_queue.get(True)
                print(new_task_from_executor)
            except Queue.Empty:
                print 'self.in_executor_queue is empty'
                break


    def get_input_queue(self):
        return self.input_queue

    def get_output_queue(self):
        return self.output_queue