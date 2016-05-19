# -*- coding: utf-8-*-
import json
from grab import GrabError
import time
from models.item_class import ItemClass
from models.steam_account_base_page import BasePage


class ItemPage(BasePage):
    def __init__(self, grab, url):
        BasePage.__init__(self, grab)
        self.grab = grab
        self.item_class = ItemClass(url=url)
        self.refresh_item_class_data()

    def get_url(self):
        return self.item_class.get_url()

    def buy_item(self):
        if self.check_value_trade_operation():
            self.remember_selling_price()
            return self.create_buy_order(self.item_class.get_highest_buy_order_in_market() + 0.03)
        return False, "Trade operation not value"

    def create_buy_order(self, price, quantity=1):
        price_total = int(price*100)
        try:
            body = {
                "appid": "730",
                "currency": "5",
                "market_hash_name": self.item_class.get_name(),
                "price_total": str(price_total),
                "quantity": str(quantity),
                "sessionid": self.grab.get_sessionid()
            }
            self.grab.setup(url="https://steamcommunity.com/market/createbuyorder/", post=body)
            self.grab.request()
            response = json.loads(self.grab.response.body)
            if response["success"] == 1:
                return True, None
            elif response["success"] == 29:
                error_message = 'This item is already in trade.'
            else:
                error_message = response
            return False, error_message
        except GrabError:
            return False, None

    def refresh_item_class_data(self):
        try:
            url_price = "http://steamcommunity.com/market/itemordershistogram?country=RU&language=russian&currency=5&" \
                        "item_nameid=%s&two_factor=0" % self.item_class.get_item_nameid()
            self.grab.setup(url=url_price)
            self.grab.request()
            responce = json.loads(self.grab.response.body)
            lowest_sell_price = float(responce['lowest_sell_order'])/100
            highest_buy_order = float(responce['highest_buy_order'])/100
            self.item_class.set_lowest_sell_price_in_market(lowest_sell_price)
            self.item_class.set_highest_buy_order_in_market(highest_buy_order)

            # print responce["buy_order_graph"][0]
            # print responce["sell_order_graph"][0]

            if responce["success"] == 1:
                return True
            else:
                return False
        except Exception as inst:
            print type(inst)
            print inst
            return False

    def check_value_trade_operation(self):
        checker = False
        i = 0
        while not checker or i > 2:
            checker = self.refresh_item_class_data()
            if not checker:
                i += 1
                time.sleep(4)
                continue
            return True  #!!!!!
            # if self.item_class.get_profit() > 0:
            #     return True
            # else:
            #     return False
        return False

    def remember_selling_price(self):
        self.item_class.set_selling_price(self.item_class.get_lowest_sell_price_in_market()-0.03)
