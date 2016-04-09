# -*- coding: utf-8-*-


class ItemClass:
    def __init__(self, class_id, name, market_link, item_nameid,
                 buy_orders=None,
                 sell_prices=None,
                 lowest_sell_price=0,
                 highest_buy_order=0,
                 profit=0,
                 ):
        self.__name = name
        self.__class_id = class_id
        self.__market_link = market_link
        self.__item_nameid = item_nameid

        self.buy_orders = buy_orders # This field not use now. For future.
        self.sell_prices = sell_prices # This field not use now. For future.
        self.lowest_sell_price = lowest_sell_price
        self.highest_buy_order = highest_buy_order
        self.profit = profit

    def set_lowest_sell_price(self, lowest_sell_price, refresh_profit_flag=False):
        self.lowest_sell_price = lowest_sell_price
        if refresh_profit_flag:
            self._calculate_profit()

    def set_highest_buy_order(self, highest_buy_order, refresh_profit_flag=False):
        self.highest_buy_order = highest_buy_order
        if refresh_profit_flag:
            self._calculate_profit()

    def get_name(self):
        return self.__name

    def get_class_id(self):
        return self.__class_id

    def get_market_link(self):
        return self.__market_link

    def get_item_nameid(self):
        return self.__item_nameid

    def get_lowest_sell_price(self):
        return self.lowest_sell_price

    def get_highest_buy_order(self):
        return self.highest_buy_order

    def get_profit(self):
        return self.profit

    def _calculate_profit(self):
        self.profit = ((self.lowest_sell_price-0.03)/1.15) - (self.highest_buy_order + 0.03)
