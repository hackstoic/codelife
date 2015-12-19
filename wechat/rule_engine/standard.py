#encoding=utf-8
from wechat.rule_engine.base import Base
from wechat.rule_interpreter.parser import parser_number_keyword,\
    parser_command_keyword,\
    parser_tag_keyword,\
    parser_other_keyword, \
    parser_special_keyword
from wechat.models import Tag, Setting
import logging
import re

# rule_log = logging.getLogger("wechat_rule")
logger = logging.getLogger("wechat")


def detect_keyword_type(keyword):
    if re.match(r'\d+$', keyword):
        return "number"
    elif re.match(r'^[a-z]+$', keyword):
        if Tag.objects.filter(tag_name=keyword):
            return "command"
        else:
            return "other"
    elif Tag.objects.filter(tag_name=keyword):
        return "tag"
    elif keyword in Setting.objects.get_value_by_key("keyword_action_map"):
        return "special"
    else:
        return "other"


class NumberKeyword(Base):
    def execute(self):
        if  detect_keyword_type(self.keyword) is "number":
            parser_number_keyword(self.keyword, self.wechat_obj)


class CommandKeyword(Base):
    def execute(self):
        if  detect_keyword_type(self.keyword) is "command":
            parser_command_keyword(self.keyword, self.wechat_obj)


class TagKeyword(Base):
    def execute(self):
        if  detect_keyword_type(self.keyword) is "tag":
            parser_tag_keyword(self.keyword, self.wechat_obj)


class SpecialKeyword(Base):
    def execute(self):
        if  detect_keyword_type(self.keyword) is "special":
            logger.info("rule-----[SpecialKeyword]")
            parser_special_keyword(self.keyword, self.wechat_obj)


class OtherKeyword(Base):
    def execute(self):
        if  detect_keyword_type(self.keyword) is "other":
            logger.info("rule-----[OtherKeyword]")
            parser_other_keyword(self.keyword, self.wechat_obj)
