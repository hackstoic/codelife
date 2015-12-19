#encoding=utf-8
from abc import abstractmethod


class Base(object):
    def __init__(self, keyword, wechat_obj):
        self.keyword = keyword
        self.wechat_obj = wechat_obj

    @abstractmethod
    def execute(self):
        pass

