# -*- coding: utf-8-*-
import os

from tables.itemclasslist import ItemClassList
from items.itemclass import ItemClass


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
