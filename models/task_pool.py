# -*- coding: utf-8-*-
import random
import threading
import time
import datetime
from models.tasks.base_task import BaseTask
from models.tasks.test_task import TestTask


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

    def len(self):
        return len(self.task_pool)


if __name__ == '__main__':
    ar = TaskPool()

    def append():
        for i in xrange(100):
            task = BaseTask(priority=random.randint(2,10))
            ar.append(task)

    append()

    for task in ar.task_pool:
        print "%s - %s" % (task.get_priority(), task.get_start_at_time())

    print ar.len()
    print '---'
    actual_task2 = ar.get_actual_task()
    if actual_task2:
        print "%s - %s" % (actual_task2.get_priority(), actual_task2.get_start_at_time())
    print ar.len()
    actual_task2 = ar.get_actual_task()
    if actual_task2:
        print "%s - %s" % (actual_task2.get_priority(), actual_task2.get_start_at_time())
    print ar.len()