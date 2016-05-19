# -*- coding: utf-8-*-
import json
import urllib
from models.item import Item
from models.steam_account_base_page import BasePage


class InventoryPage(BasePage):
    def __init__(self, grab):
        BasePage.__init__(self, grab)
        self.grab = grab
        self.__items = list()

    def refresh_items(self):
        checker, data = self.__request_csgo_data_from_steam()
        if not data["rgDescriptions"]:
            return False, "Inventory is empty"
        if checker:
            del self.__items[:]
            init_data = self.__parse_data(data)
            for item in init_data:
                self.__items.append(Item(
                    grab=self.grab,
                    id=item["id"],
                    name=item["market_hash_name"],
                    url=item["url"],
                    pos=item["pos"]
                ))
            return True
        return False

    def __request_csgo_data_from_steam(self):
        try:
            self.grab.go('http://steamcommunity.com/profiles/'+self.grab.steam_id+'/inventory/json/730/2/')
            str_response_body = self.grab.response.body
            response_body = json.loads(str_response_body)
            return True, response_body
        except StandardError:
            return False, None

    @staticmethod
    def __parse_data(data):
        result_list = list()
        temp_dict = {}
        for item in data["rgInventory"]:
            temp_dict["id"] = data["rgInventory"][item]["id"]
            temp_dict["class_id"] = data["rgInventory"][item]["classid"]
            temp_dict["pos"] = data["rgInventory"][item]["pos"]
            for classid in data["rgDescriptions"]:
                if data["rgDescriptions"][classid]["classid"] == data["rgInventory"][item]["classid"]:
                    temp_dict['market_hash_name'] = data["rgDescriptions"][classid]["market_hash_name"]
                    url = urllib.quote(data["rgDescriptions"][classid]["market_hash_name"])
                    url = "http://steamcommunity.com/market/listings/730/" + url
                    temp_dict["url"] = url
                    break
            result_list.append(temp_dict.copy())

        def sort_by_pos(input_dict):
            return input_dict["pos"]
        result_list.sort(key=sort_by_pos)
        return result_list

    def exist_item_with_url(self, url):
        for item in self.__items:
            if item.get_url() == url:
                return True
        return False

    def get_item_by_url(self, url):
        for item in self.__items:
            if item.get_url() == url:
                return item
        return None

    def get_list_all_items(self):
        return self.__items
