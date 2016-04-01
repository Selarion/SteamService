# -*- coding: utf-8-*-

from grab import Grab


class Snatcher():
    def __init__(self):
        pass

    def test(self, input_queue, output_queue):
        print 'snatcher thread is start'
        while True:
            item_nameid = input_queue.get()
            output_queue.put(item_nameid)