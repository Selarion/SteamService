# -*- coding: utf-8-*-
import threading
import time


class Test:
    status = '!'

    def __init__(self):
        pass

    def run(self, write):
        time.sleep(2)
        self.status = "test"+write

    def write(self):
        print self.status



if __name__ == '__main__':
    t = Test()
    test_th1 = threading.Thread(target=t.run, args=['123'])
    test_th2 = threading.Thread(target=t.run, args=['321'])

    test_th1.start()
    test_th2.start()

    test_th1.join()
    test_th2.join()

    t.write()