# -*- coding: utf-8-*-
from peewee import *

from models.basemodel import BaseModel
from models.item_class import ItemClass


class ItemClassTable(BaseModel):
    class_id = IntegerField(primary_key=True)
    name = CharField()
    market_link = CharField()
    item_nameid = CharField()
    actual_price = DoubleField()
    update_time = DateTimeField()
    create_time = DateTimeField()

    @staticmethod
    def get_default_itemclass_list():
        select_query = ItemClassTable.select()
        result_list = []
        for class_item in select_query:
            if ('|' in class_item.name) and ('Sticker' not in class_item.name) and ('Autograph' not in class_item.name):
                result_list.append(ItemClass(name=class_item.name,
                                             class_id=class_item.class_id,
                                             market_link=class_item.market_link,
                                             item_nameid=class_item.item_nameid))
        return result_list

    class Meta:
        db_table = 'item_classes'
