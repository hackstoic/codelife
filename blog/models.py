#encoding=utf-8
from django.db import models
from DjangoUeditor.models import UEditorField


# Create your models here.
class Tag(models.Model):
    tag_name = models.CharField(max_length=20)
    create_time = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.tag_name


class Classification(models.Model):
    name = models.CharField(max_length=20)

    def __unicode__(self):
        return self.name


class Author(models.Model):
    name = models.CharField(max_length=30)
    email = models.EmailField(blank=True)
    website = models.URLField(blank=True)

    def __unicode__(self):
        return u'%s' % (self.name)


class Article(models.Model):
    caption = models.CharField(max_length=30)
    subcaption = models.CharField(max_length=50, blank=True)
    publish_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(Author)
    classification = models.ForeignKey(Classification)
    tags = models.ManyToManyField(Tag, blank=True)
    content = UEditorField(u'内容   ',width=600, height=600, toolbars="full", imagePath="images/",
                           filePath="docs/",
                           upload_settings={"imageMaxSize":1204000},
                           settings={},command=None,blank=True)
    publish_or_not = models.BooleanField("是否要发表？", default=False)


class Resume(models.Model):
    name = models.CharField("resume name", max_length=30)
    content = UEditorField(u'内容   ',width=600, height=600, toolbars="full", imagePath="images/",
                           filePath="docs/",
                           upload_settings={"imageMaxSize":1204000},
                           settings={},command=None,blank=True)
    show_or_not = models.BooleanField("是否要发表？", default=False)
    last_update = models.DateTimeField(auto_now_add=True)