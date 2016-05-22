# -*- coding: utf-8-*-
import random
import threading
import time
import datetime

from models.tasks.base_task import BaseTask


class TaskPool:

    @classmethod
    def _sort_by_priority(cls, a):
        return a.get_priority(), a.get_start_at_time()

    def __init__(self):
        self.__lock = threading.RLock()
        self.task_pool = list()

    def append(self, new_task):
        if not isinstance(new_task, BaseTask):
            raise TypeError('Only instance of class "Task" can be append')
        with self.__lock:
            time.sleep(random.uniform(0, 0.1))
            self.task_pool.append(new_task)
            self.task_pool.sort(key=self._sort_by_priority)

    def get_actual_task(self):
        with self.__lock:
            for actual_task in self.task_pool:
                if datetime.datetime.now() >= actual_task.get_start_at_time():
                    answer = actual_task
                    self.task_pool.remove(actual_task)
                    return answer
            return None

    def is_emty(self):
        with self.__lock:
            if self.len() == 0:
                return True
            return False

    def len(self):
        return len(self.task_pool)
