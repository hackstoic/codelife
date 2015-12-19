# -*- coding: utf8 -*-

from django.db import models
from DjangoUeditor.models import UEditorField
import json
# Create your models here.


class Tag(models.Model):
    tag_name = models.CharField(max_length=20)
    create_time = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.tag_name


class ImageText(models.Model):
    title = models.CharField("标题", max_length=40, unique=True )
    description = models.CharField("描述", max_length=120, blank=True)
    picurl = models.URLField("图片链接", blank=True)
    url = models.URLField("图文跳转链接")
    tags = models.ManyToManyField(Tag, blank=True)
    content = UEditorField(u'内容   ', width=600, height=600, toolbars="full", imagePath="images/",
                           filePath="docs/",
                           upload_settings={"imageMaxSize": 1204000},
                           settings={}, command=None, blank=True)

    origin_url = models.URLField("原文链接", blank=True)


class Response(models.Model):
    """
        存储回应内容，回复内容前，先在这里查找是否有对应的内容，没有的话，再新生成一个
    """
    keyword = models.CharField(max_length=80)
    content = models.TextField()
    md5_value = models.CharField(max_length=100)
    last_update = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.keyword


class Message(models.Model):
    context = models.CharField(max_length=100)
    add_time = models.DateTimeField(auto_now_add=True)


class LinuxCmd(models.Model):
    name = models.CharField("命令名称", max_length=20, unique=True )
    tags = models.ManyToManyField(Tag, blank=True)
    brief = models.TextField("命令简介", max_length=600)
    content = UEditorField(u'内容   ', width=600, height=600, toolbars="full", imagePath="images/",
                           filePath="docs/",
                           upload_settings={"imageMaxSize": 1204000},
                           settings={}, command=None, blank=True)

    url = models.URLField("参考资源", blank=True)

TYPE = (
    ("str", "string"),
    ("int", "int"),
    ("int", "boolean"),
    ("float", "float"),
    ("json", "json")
)


class SettingManager(models.Manager):

    def get_value_by_key(self, key):
        try:
            model = self.model.objects.get(key=key)
            if model.type == "json":
                return json.loads(model.value)
            return eval(model.type)(model.value)
        except self.model.DoesNotExist:
            return None
        except UnicodeEncodeError:
            return model.value

    def set_value_by_key(self, key, value, key_type=None):
        if key_type is None:
            if isinstance(value, dict) or isinstance(value, list):
                key_type = "json"
                value = json.dumps(value)
            else:
                key_type = type(value).__name__
        try:
            model = self.model.objects.get(key=key)
            model.value = value
            model.type = key_type
            model.save()
        except self.model.DoesNotExist:
            self.model(key=key, value=value, type=key_type).save()
        return True


class Setting(models.Model):
    key = models.CharField(max_length=255, unique=True)
    value = models.TextField(null=True, blank=True)
    type = models.CharField(choices=TYPE, help_text="key类型", max_length=50)
    is_enabled = models.BooleanField(default=True, help_text="是否启用该配置")
    is_scheduled = models.BooleanField(default=True,blank=True, help_text="是否启用计划时间， 不启用则默认永久有效")
    start_time = models.DateTimeField(verbose_name="配置生效开始时间", blank=True, null=True)
    end_time = models.DateTimeField(verbose_name="配置生效结束时间", blank=True, null=True)
    brief = models.TextField(help_text="帮助说明", blank=True)
    add_time = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)
    objects = SettingManager()

    def __unicode__(self):
        return "%s" % self.key
