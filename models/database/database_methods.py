# -*- coding: utf-8-*-

from models.database.tables.itemclasslist import ItemClassList
from models.database.tables.steamaccountslist import SteamAccountsList

from models.steamaccounts.steam_account import SteamAccount
from models.item.itemclass import ItemClass


def get_default_itemclass_list():
    select_query = ItemClassList.select()
    result_list = []
    for class_item in select_query:
        if ('|' in class_item.name) and ('Sticker' not in class_item.name) and ('Autograph' not in class_item.name):
            result_list.append(ItemClass(
                name=class_item.name,
                class_id=class_item.class_id,
                market_link=class_item.market_link,
                item_nameid=class_item.item_nameid
            ))
    return result_list


def get_steam_account_list():
    select_query = SteamAccountsList.select()
    result_list = []
    for account in select_query:
        result_list.append(SteamAccount(login_steam=account.login_steam,
                                        pass_steam=account.pass_steam,
                                        code_link=account.code_link))
    return result_list
