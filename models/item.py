# -*- coding: utf-8-*-
import json


class Item(object):
    def __init__(self, grab, id, name, url, pos):
        self.__grab = grab
        self.__id = id
        self.__name = name
        self.__url = url
        self.__pos = pos

    def sell_item(self, price):
        try:
            post = {
                "sessionid": self.__grab.get_sessionid(),
                "appid": "730",
                "contextid": "2",
                "assetid": self.__id,
                "amount": "1",
                "price": str(int(round(price/1.15, 2)*100))
            }
            url = "https://steamcommunity.com/market/sellitem/"
            self.__grab.setup(url=url, post=post)
            self.__grab.request()
            response = json.loads(self.__grab.response.body)
            if response["success"]:
                return True, None
            else:
                return False, response["message"]
        except StandardError:
            return False, "Error when buying"

    def get_id(self):
        return self.__id

    def get_name(self):
        return self.__name

    def get_url(self):
        return self.__url

    def get_pos(self):
        return self.__pos
