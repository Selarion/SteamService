# -*- coding: utf-8-*-
from models.steam_account_item_page import ItemPage


class ItemPagesList:
    def __init__(self, steam_account):
        self.steam_account = steam_account
        self.__item_pages = list()

    def create_page(self, url):
        return ItemPage(self.steam_account.grab, url)

    def append_page(self, item_page):
        # Checking for uniqueness
        if self.__item_pages:
            for page in self.__item_pages:
                if page.get_url() == item_page.get_url():
                    return None
        self.__item_pages.append(item_page)

    def create_and_append_page(self, url):
        self.append_page(self.create_page(url))

    def exist_page_with_url(self, url):
        for page in self.__item_pages:
            if page.get_url() == url:
                return True
        return False

    def get_page_by_url(self, url):
        for page in self.__item_pages:
            if page.get_url() == url:
                return page
        return None

    def get_list_all_pages(self):
        return self.__item_pages

#
# if __name__ == '__main__':
#     it = ItemPagesList()
#     a = it.create_page('123')
#     it.append_page(a)
#     it.create_and_append_page('321')
#     it.create_and_append_page('321')
