# -*- coding: utf-8-*-
import webbrowser
import math


class Foo:
    def __init__(self, number):
        self.number = number

    def get_number(self):
        return self.number

if __name__ == '__main__':
    n = str(1000600007000000)
    i = 0
    max = 0
    for j in n:
        if j == "0":
            i += 1
        else:
            i = 0
        if i > max:
                max = i
    print max
