# -*- coding: utf-8-*-
from peewee import *

from models.basemodel import BaseModel
from models.steam_account import SteamAccount


class SteamAccountsTable(BaseModel):
    id = IntegerField()
    login_steam = CharField()
    pass_steam = CharField()
    code_link = CharField()

    @staticmethod
    def get_steam_account_list():
        select_query = SteamAccountsTable.select()
        result_list = []
        for account in select_query:
            result_list.append(SteamAccount(login_steam=account.login_steam,
                                            pass_steam=account.pass_steam,
                                            code_link=account.code_link))
        return result_list

    class Meta:
        db_table = 'steam_accounts'