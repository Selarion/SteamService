# -*- coding: utf-8-*-
import os
from peewee import *


def take_logpass_from_file():
    with open('../conf/db_info.txt') as f:
        data = f.read().split(',')
        for i in range(len(data)):
            word = data[i].strip()
            word = word.split('=')
            if word[0] == 'database':
                database = word[1]
            elif word[0] == 'user':
                user = word[1]
            elif word[0] == 'password':
                password = word[1]
            elif word[0] == 'host':
                host = word[1]
            else:
                raw_input('Data_base file is bad.')
        return database, user, password, host

data = take_logpass_from_file()
mysql_db = MySQLDatabase(database=data[0], user=data[1], password=data[2], host=data[3])


class BaseModel(Model):
    class Meta:
        database = mysql_db

if __name__ == '__main__':
    print(os.getcwd())