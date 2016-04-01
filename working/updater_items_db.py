# -*- coding: utf-8-*-
import json
import re
import time
import datetime
import logging

import peewee
from grab import Grab

from database import basemodel

logger = logging.getLogger('grab')
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)

class Main():
    url_market = "http://steamcommunity.com/market/search/render/?query=&search_descriptions=0&sort_column=quantity&sort_dir=desc"

    def __init__(self, appid):
        self.appid = appid
        self.url_market += self.appid

    def start(self, start, stop, count):
        g = Grab()
        g.setup(debug_post=True)
        for i in range(start, stop, count):
            url_market = self.url_market
            start_str = "&start=" + str(i)
            count_str = "&count=" + str(count)
            url_market += start_str
            url_market += count_str

            print '------'
            while True:
                try:
                    g.setup(url=url_market)
                    g.request()
                    responce = json.loads(g.response.body)

                    parser = Grab(responce["results_html"].encode('utf-8'))
                    g2 = Grab()
                except:
                    time.sleep(30)
                    continue
                for item in parser.doc.select(".//*[@class='market_listing_row_link']"):
                    while True:
                        try:
                            g3 = Grab()

                            name = item.select(".//div[1]/div[2]/span[1]").text()
                            link = item.select(".//@href").text()

                            try:
                                i = basemodel.Itemclass_list.get(basemodel.Itemclass_list.name == name)
                                print '1'
                                print i.name
                                break
                            except:
                                print '2'
                                print name
                            g2.setup(url=link)
                            g2.request()
                            item_nameid = re.findall("Market_LoadOrderSpread\(\s*(\d+)\s*\)", g2.response.body)[0]
                            class_id = int(re.findall('classid":"(.+?)"', g2.response.body)[0])

                            url_price = "steamcommunity.com/market/itemordershistogram?country=RU&language=russian&currency=5&item_nameid=%s&two_factor=0" % item_nameid

                            g3.setup(url=url_price)
                            g3.request()

                            price = json.loads(g3.response.body)['lowest_sell_order']

                            record = basemodel.Itemclass_list()
                            record.class_id = class_id
                            record.name = name
                            record.market_link = link
                            record.item_nameid = item_nameid
                            record.actual_price = float(price)/100
                            record.update_time = datetime.datetime.now()
                            record.create_time = datetime.datetime.now()

                            time.sleep(2)

                            record.save(force_insert=True)
                            break

                        except(peewee.IntegrityError) as e:
                            print '!!!'
                            break
                        except(Exception) as e:
                            print e
                            time.sleep(30)
                            continue
                break

if __name__ == '__main__':
    bot = Main("&appid=730")
    bot.start(20, 620, 50)

#http://steamcommunity.com/market/itemordershistogram?country=RU&language=russian&currency=1&item_nameid=8988621&two_factor=0
#http://steamcommunity.com/market/listings/730/steamcommunity.com/market/itemordershistogram?country=RU&language=russian&currency=5&item_nameid=8988621&two_factor=0