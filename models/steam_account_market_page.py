# -*- coding: utf-8-*-
import traceback
from grab import GrabError

from models.steam_account_base_page import BasePage


class MarketPage(BasePage):
    def __init__(self, steam_account):
        BasePage.__init__(self, steam_account.grab)
        self.steam_account = steam_account
        self.my_sell_orders = None
        self.my_buy_orders = None

    def goto_market_page(self):
        self.grab.setup(url="http://steamcommunity.com/market/")
        try:
            self.grab.request()
        except GrabError:
            pass
        return self.check_login()

    def get_market_page_data(self):
        checker = self.goto_market_page()
        sell_order_list = list()
        buy_order_list = list()
        balance = float()
        if checker:
            balance = float(self.grab.doc.select(".//*[@id='marketWalletBalanceAmount']").text()[:-5].replace(",", "."))
            for el in self.grab.doc.select(".//*[@id='tabContentsMyListings']/div[1]/*[starts-with(@id,'mylisting')]"):
                sell_order = dict()
                sell_order["code_link"] = el.select(".//div[4]/span[1]/a").attr('href')
                sell_price = el.select(".//span/span/span/span[1]").text().split(" ")[-2]
                sell_order["sell_price"] = float(sell_price.replace(",", "."))
                sell_price_without_fee = el.select(".//span/span/span/span[2]").text().split(" ")[-2][1:]
                sell_order["sell_price_without_fee"] = float(sell_price_without_fee.replace(",", "."))
                sell_order['order_id'] = el.attr('id').split("_")[1]
                sell_order_list.append(sell_order)

            for el in self.grab.doc.select(".//*[@id='tabContentsMyListings']/div[2]/*[starts-with(@id,'mybuyorder')]"):
                buy_order = dict()
                buy_order["code_link"] = el.select(".//div[4]/span[1]/a").attr('href')
                buy_price = el.select(".//div[2]/span/span").text().split(" ")[-2]
                buy_order["buy_price"] = float(buy_price.replace(",", "."))
                buy_order['order_id'] = el.attr('id').split("_")[1]
                buy_order_list.append(buy_order)
            return True, balance, sell_order_list, buy_order_list
        else:
            return False, balance, sell_order_list, buy_order_list

    def refresh_market_page_data(self):
        checker, balance, sell_order_list, buy_order_list  = self.get_market_page_data()
        if checker:
            self.steam_account.set_balance(balance)
            self.my_sell_orders = sell_order_list
            self.my_buy_orders = buy_order_list
            return True
        else:
            return False

    def refresh_and_compare_market_page_data(self):
        checker, balance, sell_order_list, buy_order_list = self.get_market_page_data()
        if checker:
            new_data = False
            added_sell_order = [order for order in sell_order_list if order not in  self.my_sell_orders]
            remove_sell_order = [order for order in self.my_sell_orders if order not in sell_order_list]
            added_buy_order = [order for order in buy_order_list if order not in self.my_buy_orders]
            remove_buy_order = [order for order in self.my_buy_orders if order not in buy_order_list]
            if added_sell_order or remove_sell_order:
                self.my_sell_orders = sell_order_list
                new_data = True
            if added_buy_order or remove_buy_order:
                self.my_buy_orders = buy_order_list
                new_data = True
            return new_data, added_sell_order, remove_sell_order, added_buy_order, remove_buy_order
        else:
            return False, None, None, None, None

    def remove_sell_order(self, order_id):
        try:
            url = "http://steamcommunity.com/market/removelisting/%s" % order_id
            self.grab.request(url=url, post={"sessionid": self.grab.get_sessionid()})
            return True, None
        except StandardError:
            error_message = traceback.format_exc()
            return False, error_message

    def remove_buy_order(self, order_id):
        try:
            url = "http://steamcommunity.com/market/cancelbuyorder/"
            self.grab.request(url=url, post={"sessionid": self.grab.session_id, "buy_orderid": order_id})
            return True, None
        except StandardError:
            error_message = traceback.format_exc()
            return False, error_message
