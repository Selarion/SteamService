# -*- coding: utf-8-*-
import random
import threading
import time

from models.steam_account_table import SteamAccountsTable
from controllers.executor_controller import ExecutorController


class Executor:
    def __init__(self):
        self.controller = ExecutorController(self)

        self.__steam_account_list = SteamAccountsTable.get_steam_account_list()
        self.__steam_account_thread_list = list()
        # self.__start_account_threads()

    def __start_account_threads(self):
        for account in self.__steam_account_list:
            time.sleep(random.uniform(0, 2))
            thread = threading.Thread(target=account.start_waiting_new_task,
                                      name="Thread: " + account.login_steam)
            self.__steam_account_thread_list.append(thread)
        self.__steam_account_thread_list[0].__start()

    def start(self, output_queue):
        print 'executor thread is start'
        self.controller.set_output_queue(output_queue)
        self.controller.start_routing()

    def fuction1(self):
        return "response 1"

    def fuction2(self):
        return "response 2"

    def fuction3(self):
        return "response 3"

    def get_input_queue(self):
        return self.controller.get_input_queue()


if __name__ == '__main__':
    pass
