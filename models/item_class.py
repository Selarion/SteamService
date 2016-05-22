# -*- coding: utf-8-*-
from models.item_class_table import ItemClassTable


class ItemClass(object):

    @staticmethod
    def get_default_itemclass_list():
        select_query = ItemClassTable.select()
        result_list = []
        for class_item in select_query:
            if ('|' in class_item.name) and ('Sticker' not in class_item.name) and ('Autograph' not in class_item.name):
                result_list.append(ItemClass(url=class_item.market_link))
        return result_list

    def __init__(self, url):
        table_record = ItemClassTable.select().where(ItemClassTable.url == url).get()
        self.__market_link = url
        self.__name = table_record.name
        self.__class_id = table_record.class_id
        self.__item_nameid = table_record.item_nameid

        self.buy_order_graph = float()  # This field not use now. For future.
        self.sell_order_graph = float()  # This field not use now. For future.
        self.lowest_sell_price_in_market = float()
        self.highest_buy_order_in_market = float()
        self.profit = float()

        self.buying_price = float()
        self.selling_price = float()

    def set_lowest_sell_price_in_market(self, lowest_sell_price):
        self.lowest_sell_price_in_market = lowest_sell_price
        self.profit = None

    def set_highest_buy_order_in_market(self, highest_buy_order):
        self.highest_buy_order_in_market = highest_buy_order
        self.profit = None

    def set_buying_price(self, price):
        self.buying_price = price

    def set_selling_price(self, price):
        self.selling_price = price

    def get_name(self):
        return self.__name

    def get_class_id(self):
        return self.__class_id

    def get_url(self):
        return self.__market_link

    def get_item_nameid(self):
        return self.__item_nameid

    def get_lowest_sell_price_in_market(self):
        return self.lowest_sell_price_in_market

    def get_highest_buy_order_in_market(self):
        return self.highest_buy_order_in_market

    def get_buying_price(self):
        return self.buying_price

    def get_selling_price(self):
        return self.selling_price

    def get_profit(self):
        if self.profit is None:
            self._calculate_profit()
        return self.profit

    def _calculate_profit(self):
        self.profit = ((self.lowest_sell_price_in_market-0.03)/1.15) - (self.highest_buy_order_in_market + 0.03)


if __name__ == '__main__':
    print ItemClass.get_default_itemclass_list()
