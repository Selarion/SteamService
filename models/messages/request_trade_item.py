# -*- coding: utf-8-*-
from models.item_class import ItemClass
from models.messages.base_message import BaseMessage


class RequestTradeItem(BaseMessage):
    def __init__(self, item_class):
        BaseMessage.__init__(self, 'No name', 'No name')
        if not isinstance(item_class, ItemClass):
            raise TypeError('"itemclass" field must be type ItemClass(), not %s' % type(item_class))
        self.item_class = item_class

    def get_item_class(self):
        return self.item_class
