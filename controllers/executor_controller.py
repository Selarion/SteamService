# -*- coding: utf-8-*-
import Queue

class ExecutorController:
    def __init__(self, executor):
        self.executor = executor
        self.input_queue = Queue.Queue()
        self.output_queue = None

    def start_routing(self):
        while True:
            try:
                new_incoming_task = self.input_queue.get()
                self.rout_task(new_incoming_task)
            except Queue.Empty:
                pass

    def rout_task(self, new_task):
        print "new_task is " + str(new_task)
        if new_task == 1:
            answer = self.executor.fuction1()
            self.output_queue.put(answer)
        elif new_task == 2:
            answer = self.executor.fuction2()
            self.output_queue.put(answer)
        elif new_task == 3:
            answer = self.executor.fuction3()
            self.output_queue.put(answer)

    def get_input_queue(self):
        return self.input_queue

    def set_output_queue(self, output_queue):
        self.output_queue = output_queue