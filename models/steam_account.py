# -*- coding: utf-8-*-
import Queue
import json

import logging
import threading
import time

from controllers.steam_account_controller import SteamAccountController
from models.item_class import ItemClass
from models.messages.request_trade_item import RequestTradeItem

from models.steam_account_grab import SteamAccountGrab
from models.steam_account_market_page import MarketPage
from models.steam_account_item_pages_list import ItemPagesList
from models.steam_account_inventory_page import InventoryPage
from models.task_pool import TaskPool

logger = logging.getLogger('grab')
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)


class SteamAccount:
    def __init__(self, login_steam, pass_steam, code_link):
        self.grab = SteamAccountGrab(self, login_steam, pass_steam, code_link)
        self.task_pool = TaskPool()
        self.controller = SteamAccountController(self.task_pool)
        self.steam_account_controller_thread = threading.Thread(target=self.controller.start_route,
                                                                name="%s SteamAccountControllerThread" % login_steam)

        self.balance = float()
        self.market_page = MarketPage(self)
        self.item_pages = ItemPagesList(self)
        self.inventory_page = InventoryPage(self.grab)

    def start(self, output_queue):
        print "Steam account %s is start!" % self.grab.login_steam
        login_answer = self.grab.login()
        marker_page_answer = self.market_page.refresh_market_page_data()
        if login_answer[0] and marker_page_answer:
            print 'login sucsess'
            self.controller.set_output_queue(output_queue)
            self.steam_account_controller_thread.start()
            self.start_main_event_loop()
        else:
            print 'login not sucsess'
            print login_answer[1]

    def start_main_event_loop(self):
        while True:
            print steam_account.task_pool.len()
            print steam_account.task_pool.get_actual_task()
            time.sleep(5)

    def check_buy_or_sell_changes(self):
        answer = self.market_page.refresh_and_compare_market_page_data()
        checker = answer[0]
        if checker:
            added_sell_order = answer[1]
            if added_sell_order:
                print '1'
            remove_sell_order = answer[2]
            if remove_sell_order:
                print '2'
            added_buy_order = answer[3]
            if added_buy_order:
                print '3'
            remove_buy_order = answer[4]
            if remove_buy_order:
                print '4'
        return checker

    def buy_item(self, item_class):
        url = item_class.get_url()
        if not self.item_pages.exist_page_with_url(url):
            self.item_pages.create_and_append_page(url)
        page = self.item_pages.get_page_by_url(url)
        sucsess_flag, error_message = page.buy_item()
        print sucsess_flag
        print error_message

    def sell_item(self, url, price):
        item = self.inventory_page.get_item_by_url(url=url)
        if item:
            success, error_mesage = item.sell_item(price=price)
            return success, error_mesage
        return False, "Item with same URL not found in inventory"

    def get_balance(self):
        return self.balance

    def set_balance(self, balance):
        self.balance = balance

    def remove_all_order(self):
        for order in self.market_page.my_sell_orders:
            self.market_page.remove_sell_order(order_id=order["order_id"])
        for order in self.market_page.my_buy_orders:
            self.market_page.remove_buy_order(order_id=order["order_id"])
        self.market_page.refresh_market_page_data()

    def sell_all_items(self):
        self.inventory_page.refresh_items()
        for item in self.inventory_page.get_list_all_items()[:-5]:
            url = item.get_url()
            self.item_pages.create_and_append_page(url)
            page = self.item_pages.get_page_by_url(url)
            price = page.item_class.get_lowest_sell_price_in_market() - 0.01

            while True:
                print "try"
                success, error_mesage = item.sell_item(price=price)
                print success
                print error_mesage
                if not success:
                    time.sleep(5)
                    continue
                break
            print "----"
        print 'all item was sent'

if __name__ == '__main__':

    item_class = ItemClass("http://steamcommunity.com/market/listings/"
                           "730/P2000%20%7C%20Amber%20Fade%20%28Field-Tested%29")

    steam_account = SteamAccount(login_steam='stl_postman_3', pass_steam='NYTuyiJ1', code_link='/bot/?id=3')
    # steam_account = SteamAccount(login_steam='stl_postman_4', pass_steam='V0NQTSn0', code_link='/bot/?id=4')
    input_queue = Queue.Queue()
    output_queue = steam_account.controller.get_input_queue()

    steam_account_thread = threading.Thread(target=steam_account.start, kwargs={'output_queue': input_queue})
    steam_account_thread.start()

    # steam_account.buy_item(item_class)
    # steam_account.check_buy_or_sell_changes()

    while True:
        task = RequestTradeItem(item_class)
        output_queue.put_nowait(task)
        print('123')
        time.sleep(1)

