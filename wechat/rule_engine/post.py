#encoding=utf-8
from wechat.rule_engine.base import Base
from wechat.rule_engine.standard import NumberKeyword, CommandKeyword, TagKeyword, OtherKeyword, SpecialKeyword


class Post(object):
    def __init__(self, keyword, wechat_obj):
        self.rules = []
        self.wechat_obj = wechat_obj
        self.keyword = keyword

    def register(self, rule_obj):
        if isinstance(rule_obj, Base):
            self.rules.append(rule_obj)
            return True
        else:
            return False

    def run(self):
        #register rules here
        number_keyword = NumberKeyword(self.keyword, self.wechat_obj)
        self.register(number_keyword)

        command_keyword = CommandKeyword(self.keyword, self.wechat_obj)
        self.register(command_keyword)

        tag_keyword = TagKeyword(self.keyword, self.wechat_obj)
        self.register(tag_keyword)

        special_keyword = SpecialKeyword(self.keyword, self.wechat_obj)
        self.register(special_keyword)

        other_keyword = OtherKeyword(self.keyword, self.wechat_obj)
        self.register(other_keyword)
        for rule in self.rules:
            rule.execute()




