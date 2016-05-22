# -*- coding: utf-8-*-
from models.tasks.base_task import BaseTask


class TaskTradeItem(BaseTask):
    def __init__(self, item_class):
        BaseTask.__init__(self)
        self.item_class = item_class

    def get_item_class(self):
        return self.item_class