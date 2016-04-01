# -*- coding: utf-8-*-

from grab import Grab

import logging
logger = logging.getLogger('grab')
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)


class Executor(Grab):
    def __init__(self):
        Grab.__init__(self)
        self.setup(log_file='default_executor_log_file.html')

    def test(self, input_queue, output_queue):
        print 'executor thread is start'


if __name__ == '__main__':
    g = Executor()
    g.go('https://www.yandex.ru/')