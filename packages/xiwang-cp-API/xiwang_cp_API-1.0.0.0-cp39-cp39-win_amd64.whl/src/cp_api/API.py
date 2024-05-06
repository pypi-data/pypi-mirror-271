# -*- coding: utf-8 -*-
class api:
    def __init__(self):
        self.__setting = None

    @property
    def setting(self):
        return self.__setting

    def __loadconf(self):
        print('1111')
