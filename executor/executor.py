# -*- coding: utf-8-*-
import Queue
import random
import threading
import time

from models.database import database_methods as db


class Executor:
    def __init__(self):
        self.steam_account_list = list()
        self.steam_account_thread_list = list()
        self.input_queue = Queue.Queue()
        self.output_queue = Queue.Queue()

        self.__load_start_data()
        self.__start_account_threads()

    def __load_start_data(self):
        self.steam_account_list = db.get_steam_account_list()

    def __start_account_threads(self):
        for account in self.steam_account_list:
            time.sleep(random.uniform(0, 2))
            thread = threading.Thread(target=account.start_waiting_new_task,
                                      name="Thread: " + account.login_steam)
            self.steam_account_thread_list.append(thread)
        self.steam_account_thread_list[0].start()

    def start_main_loop(self):
        print 'executor thread is start'

    def get_input_queue(self):
        return self.input_queue

    def get_output_queue(self):
        return self.output_queue


if __name__ == '__main__':
    execut = Executor()
    execut.steam_account_list[0].get_input_queue().put('eto rabotaet')