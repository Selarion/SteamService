# -*- coding: utf-8-*-
import random

import threading, Queue
import time


def writer(queue):
    rnd = random.uniform(0, 2)
    print "--- " + str(rnd)
    time.sleep(rnd)
    if rnd > 1.5:
        queue.put(rnd)

def main():
    threading_pool = [None]*10
    queue = Queue.Queue()

    for i in range(len(threading_pool)):
        threading_pool[i] = threading.Thread(target=writer, args=[queue])

    for thread in threading_pool:
        thread.start()

    t1 = time.time()
    while True:
        if (time.time() - t1) < 5:
            if queue.qsize() != 0:
                print queue.get()
                t1 = time.time()
        else:
            break



if __name__ == '__main__':
    main()