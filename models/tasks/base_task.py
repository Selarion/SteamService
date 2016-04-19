# -*- coding: utf-8-*-
import datetime


class BaseTask:
    id_task = 1

    def __init__(self):
        self.created_at = datetime.datetime.now()
        self.start_at = None
        self.id = self.__class__.id_task
        self.__class__.id_task += 1

    def get_created_at(self):
        return self.created_at

    def get_start_at_time(self):
        return self.start_at

    def set_start_at_time(self, start_at):
        self.start_at = start_at