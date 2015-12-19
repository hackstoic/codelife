# -*- coding: utf-8 -*-

from wechat.models import ImageText
from wechat.models import Response, Message
import hashlib
import sys
import logging
# rule_log = logging.getLogger("wechat_rule")
logger = logging.getLogger("wechat")

reload(sys)
sys.setdefaultencoding('utf8')


def save_response(keyword, response):
    """
        比较hash值，如果响应的内容没有变化，则不做保存操作；如果有变化，则更新内容
    """
    if response is None:
        return "no need to save"
    try:
        info_md5 = hashlib.md5()
        info_md5.update(response)
    except Exception as ex:
        logger.error("md5 update occur error : %s" % ex)
        return  "error"
    try:
        obj = Response.objects.get(keyword=keyword)
        if obj.md5_value == info_md5.hexdigest():
            pass
        else:
            obj.md5_value = info_md5
            obj.content = response
            obj.save()
            logger.info("update response content")
    except Response.DoesNotExist:
        msg_dict = {
            "keyword": keyword,
            "content": response,
            "md5_value": info_md5,
        }
        obj = Response(**msg_dict)
        obj.save()
        logger.info("save response content")
    except Exception as ex:
        logger.error(ex)
    return ""


def save_message(keyword):
    obj = Message(context=keyword)
    obj.save()
    logger.info("save message")
    return ""


def generate_news(keyword, wechat_obj):
    """
        图文的数量不能超过10条
    """
    try:
        a = ImageText.objects.filter(tags__tag_name=keyword)
        news = []
        if len(a) <= 0:
            response = None
            return response
        elif len(a) > 10:
            idx = 9
        else:
            idx = len(a)
        for itext in a[0:idx]:
            news.append({
                'title': itext.title,
                'description': itext.description,
                'url': itext.url,
            })
        response = wechat_obj.response_news(news)
    except Exception as ex:
        response = None
        logger.error(ex)
    return response


def generate_text(text_content, wechat_obj):
    response = wechat_obj.response_text(text_content)
    # logger.info("the Response: %s" % response)
    return response