#encoding=utf-8
"""parser module v1.0
"""
from wechat.rule_engine.action import generate_news,\
    generate_text, \
    save_response,\
    save_message
from wechat.models import LinuxCmd
import logging
import re
import hashlib
import json

# rule_log = logging.getLogger("wechat_rule")
logger = logging.getLogger("wechat")


def parser_number_keyword(keyword, wechat_obj):
    response = generate_news(keyword, wechat_obj)
    save_response(keyword, response)
    save_message(keyword)
    return ""


def parser_command_keyword(keyword, wechat_obj):
    cmd_obj = LinuxCmd.objects.get(name=keyword)
    brief = cmd_obj.brief
    content = cmd_obj.content
    url = cmd_obj.url
    brief_md5 = hashlib.md5()
    brief_md5.update(brief.strip())
    content_md5 = hashlib.md5()
    content_md5.update(content)
    if brief_md5.hexdigest() == content_md5.hexdigest():
        text_content = brief
    else:
        text_content = "%s\n\n%s" % (brief, url)  # 如果内容比较长，则返回摘要和url链接
    response = generate_text(text_content, wechat_obj)
    save_response(keyword, response)
    save_message(keyword)
    return ""


def parser_tag_keyword(keyword, wechat_obj):
    response = generate_news(keyword, wechat_obj)
    save_response(keyword, response)
    save_message(keyword)
    return ""


def parser_special_keyword(keyword, wechat_obj):
    from aws.tasks import start_ec2, stop_ec2, check_ec2
    from wechat.models import Setting
    keyword_action_map = Setting.objects.get_value_by_key("keyword_action_map")
    action = keyword_action_map[keyword]
    result = eval(action)()
    text_content = json.dumps(result)
    response = generate_text(text_content, wechat_obj)
    save_response(keyword, response)
    save_message(keyword)
    return ""


def parser_other_keyword(keyword, wechat_obj):
    if re.match(r'^h$', keyword, re.I) or re.match(r'^help$', keyword, re.I):
        text_content = "发送1，查看Linux常用命令系列文章\n" \
                       "发送2，查看Linux技巧介绍系列文章\n" \
                       "发送3，查看Linux系统原理系列文章\n" \
                       "发送4，查看Linux运维相关系列文章\n" \
                       "发送5，查看Linux职业人生系列文章\n" \
                       "发送6，查看Linux下的工具系列文章\n" \
                       "发送7，查看Linux黑客系列文章\n" \
                       "发送8，查看Linux趣味系列文章\n" \
                       "发送9，查看Linux入门介绍系列文章\n" \
                       "输入小写的linux命令，返回命令的中文man手册\n" \
                       "输入大写的linux命令，如TOP，返回相关的图文说明\n" \
                       "输入相关的关键词，如输入“监控”等，返回图文列表\n" \
                       "查看全部内容文章，点击右上角，选择查看历史消息\n" \
                       "发送“h”或者“help”，查看以上帮助信息\n"
        response = generate_text(text_content, wechat_obj)
        save_response(keyword, response)
        save_message(keyword)
    else:
        save_message(keyword)
        generate_text(u"没有对应内容。请尝试其它关键词。", wechat_obj)
    return ""

