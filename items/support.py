# -*- coding: utf-8-*-
import json
import sys


def main():
    data = [['date', 'highest_buy_order', 'lowest_sell_order'],]

    with open("3_item SSG 08 Пучина (После полевых испытаний).txt") as f:
        for line in f.readlines():
            bfr = []
            jsn = json.loads(line.rstrip())
            bfr.append(jsn['time_now'])
            bfr.append(jsn['highest_buy_order'])
            bfr.append(jsn['lowest_sell_order'])
            data.append(bfr)

        for point in data[1:]:
            pass
            sys.stdout.write("['%s', %s, %s],\n" % (point[0], point[1], point[2]))

        min = data[1][2]
        max = data[1][1]

        for point in data[1:]:
            if max < point[1]:
                max = point[1]
            if (min > point[2]) and (point[2] > 100):
                min = point[2]
                print point[0]

        print max
        print min

if __name__ == '__main__':
    main()