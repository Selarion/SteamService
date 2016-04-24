# -*- coding: utf-8-*-
import random
import threading
import time

from models.steam_account_table import SteamAccountsTable
from controllers.executor_controller import ExecutorController


class Executor:
    def __init__(self):
        self.controller = ExecutorController(self)
        self.executor_controller_thread = threading.Thread(target=self.controller.start_routing,
                                                   name='ExecutorControllerThread')

        self.steam_account_list = SteamAccountsTable.get_steam_account_list()
        self.steam_account_thread_list = list()

    def start(self, output_queue):
        print 'executor thread is start'
        self.controller.set_output_queue(output_queue)
        self.executor_controller_thread.start()
        self.start_main_event_loop()

    def start_main_event_loop(self):
        while True:
            print 'Executor main event loop'
            time.sleep(5)

    def fuction1(self):
        return "response 1"

    def get_input_queue(self):
        return self.controller.get_input_queue()


if __name__ == '__main__':
    e = Executor()
    print e.steam_account_list[0].code_link