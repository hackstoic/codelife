#coding=utf-8
from django.template import RequestContext
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from django.template import RequestContext
import json
from auto_reply import TOKEN, auto_reply
from wechat.models import LinuxCmd
import hashlib
import logging
# Create your views here.

logger = logging.getLogger("wechat")


def validate(request):
    signature = request.REQUEST.get('signature', '')
    timestamp = request.REQUEST.get('timestamp', '')
    nonce = request.REQUEST.get('nonce',  '')
    tmp_str = hashlib.sha1(''.join(sorted([TOKEN, timestamp, nonce]))).hexdigest()
    if tmp_str == signature:
        return True
    return False

@csrf_exempt
def index(request):
    signature = request.GET.get("signature", "")
    echostr = request.GET.get("echostr", "")
    timestamp = request.GET.get("timestamp", "")
    nonce = request.GET.get("nonce", "")
    logger.info("The POST is : %s" % request.body)
    body_text = request.body
    if request.method == 'GET':
        signature = request.GET.get("signature", "")
        echostr = request.GET.get("echostr", "")
        timestamp = request.GET.get("timestamp", "")
        nonce = request.GET.get("nonce", "")
        logger.info(signature, echostr, timestamp, nonce)
        print signature, echostr, timestamp, nonce
        # when first access to wechat platform , please uncomment this four lines
        if validate(request):
            return HttpResponse(echostr)
        else:
            return HttpResponse("error, 非法的微信请求！")
    else:
        response = auto_reply(signature=signature, timestamp=timestamp, nonce=nonce, body_text=body_text)
    # 现在直接将 response 变量内容直接作为 HTTP Response 响应微信服务器即可，此处为了演示返回内容，直接将响应进行输出
    return HttpResponse(response)


def cmd_tutorial_page(request, cmd):
    try:
        cmd_obj = LinuxCmd.objects.get(name=cmd)
    except LinuxCmd.DoesNotExist:
        cmd_obj = {"name": cmd, "content": "内容不存在！"}
    except Exception:
        cmd_obj = {"name": cmd, "content": "内容不存在！"}
    return render_to_response("tutorial.html", {"cmd_obj": cmd_obj},context_instance=RequestContext(request) )
