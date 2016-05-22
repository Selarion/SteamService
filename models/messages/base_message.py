# -*- coding: utf-8-*-


class BaseMessage(object):
    def __init__(self, author, addressee):
        if not isinstance(author, str):
            raise TypeError('"author" field must be type string, not %s' % type(author))
        if not isinstance(addressee, str):
            raise TypeError('"addressee" field must be type string, not %s' % type(addressee))
        self.author = author
        self.addressee = addressee
