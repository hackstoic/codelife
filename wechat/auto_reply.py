#!/usr/bin/python
# -*- coding: utf-8 -*-

from wechat_sdk import WechatExt
from wechat_sdk import WechatBasic
from wechat_sdk.messages import (
    TextMessage, VoiceMessage, ImageMessage, VideoMessage, LinkMessage, LocationMessage, EventMessage
)
from rule_engine.post import Post
from wechat.models import Response
from wechat.rule_engine.action import  save_message
import  logging
from codelife.private import WECHAT_TOKEN
TOKEN = WECHAT_TOKEN

logger = logging.getLogger("wechat")


def auto_login():
    wechat = WechatExt(login=False, username='', password='', ifencodepwd=True)
    print wechat
    r = wechat.login()
    print r
    pass


def auto_reply(signature, timestamp, nonce, body_text):
    # 实例化 wechat
    wechat = WechatBasic(token=TOKEN)
    # 对签名进行校验
    if wechat.check_signature(signature=signature, timestamp=timestamp, nonce=nonce):
        # 对 XML 数据进行解析 (必要, 否则不可执行 response_text, response_image 等操作)
        wechat.parse_data(body_text)
        # 获得解析结果, message 为 WechatMessage 对象 (wechat_sdk.messages中定义)
        message = wechat.get_message()
        response = None
        if isinstance(message, TextMessage):
            keyword = message.content
            try:
                P = Post(keyword, wechat)
                P.run()
            except Exception as ex:
                response = wechat.response_text(content=u'无查询结果，请尝试其它关键词。输入h，查看帮助。')
                logger.exception(ex)
            try:
                response = Response.objects.get(keyword=keyword).content
                logger.info("auto reply response")
            except Exception as ex:
                response = wechat.response_text(content=u'无查询结果，请尝试其它关键词。输入h，查看帮助。')
                logger.error(ex)

        elif isinstance(message, VoiceMessage):
            save_message("VoiceMessage")
            response = wechat.response_text(content=u'语音信息')
        elif isinstance(message, ImageMessage):
            save_message("ImageMessage")
            response = wechat.response_text(content=u'图片信息')
        elif isinstance(message, VideoMessage):
            save_message("VideoMessage")
            response = wechat.response_text(content=u'视频信息')
        elif isinstance(message, LinkMessage):
            save_message("LinkMessage")
            response = wechat.response_text(content=u'链接信息')
        elif isinstance(message, LocationMessage):
            save_message("LocationMessage")
            response = wechat.response_text(content=u'地理位置信息')
        elif isinstance(message, EventMessage):  # 事件信息
            if message.type == 'subscribe':  # 关注事件(包括普通关注事件和扫描二维码造成的关注事件)
                if message.key and message.ticket:  # 如果 key 和 ticket 均不为空，则是扫描二维码造成的关注事件
                    response = wechat.response_text(content=u'用户尚未关注时的二维码扫描关注事件')
                else:
                    reply_text = u"你好！感谢关注linux-world公众号。" \
                                 u"让我们一起感受Linux的魅力，享受学习的乐趣吧！" \
                                 u"发送“h”或者“help”，查看相关帮助信息。" \
                                 u"点击右上角，查看历史信息，发现精彩内容。" \
                                 u"目前微信平台在开发之中，后期会推出更加精彩的功能和内容。"
                    # response = wechat.response_text(content=u'普通关注事件')
                    response = wechat.response_text(content=reply_text)
            elif message.type == 'unsubscribe':
                response = wechat.response_text(content=u'取消关注事件')
            elif message.type == 'scan':
                response = wechat.response_text(content=u'用户已关注时的二维码扫描事件')
            elif message.type == 'location':
                response = wechat.response_text(content=u'上报地理位置事件')
            elif message.type == 'click':
                response = wechat.response_text(content=u'自定义菜单点击事件')
            elif message.type == 'view':
                response = wechat.response_text(content=u'自定义菜单跳转链接事件')
    else:
        response = "error, 非法的微信请求！"
    return response

if __name__ == "__main__":
    auto_login()
