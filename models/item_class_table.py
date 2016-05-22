# -*- coding: utf-8-*-
from peewee import *

from models.basemodel import BaseModel


class ItemClassTable(BaseModel):
    class_id = IntegerField(primary_key=True)
    name = CharField()
    url = CharField()
    item_nameid = CharField()
    actual_price = DoubleField()
    update_time = DateTimeField()
    create_time = DateTimeField()

    class Meta:
        db_table = 'item_classes'
