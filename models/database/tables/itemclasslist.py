# -*- coding: utf-8-*-
from peewee import *

from models.database.basemodel import BaseModel


class ItemClassList(BaseModel):
    class_id = IntegerField(primary_key=True)
    name = CharField()
    market_link = CharField()
    item_nameid = CharField()
    actual_price = DoubleField()
    update_time = DateTimeField()
    create_time = DateTimeField()

    class Meta:
        db_table = 'itemclass_list'