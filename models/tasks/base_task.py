# -*- coding: utf-8-*-
import datetime


class BaseTask:
    def __init__(self, priority=1):
        if not isinstance(priority, int):
            raise TypeError('"Priority" field must be type "integer"')
        self.__priority = priority
        self.__created_at = datetime.datetime.now()
        self.__start_at = datetime.datetime.now()

    def get_priority(self):
        return self.__priority

    def get_created_at(self):
        return self.__created_at

    def get_start_at_time(self):
        return self.__start_at

    def set_priority(self, priority):
        if not isinstance(priority, int):
            raise TypeError('"Priority" field must be type "integer"')
        self.__priority = priority

    def set_start_at_time(self, start_at):
        self.__start_at = start_at