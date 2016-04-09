# -*- coding: utf-8-*-
from peewee import *

from models.database.basemodel import BaseModel


class SteamAccountsList(BaseModel):
    id = IntegerField()
    login_steam = CharField()
    pass_steam = CharField()
    code_link = CharField()

    class Meta:
        db_table = 'steam_accounts_list'