# coding=utf8
from django.shortcuts import render
from blog.models import Article, Tag, Classification, Resume
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import Http404
from datetime import datetime
# Create your views here.
try:
    from ipdb import set_trace
except:
    pass


def blog_list(request):
    archive_date = request.GET.get("archive_date", None)
    classified = request.GET.get("classified", None)
    date_list = []
    cls_list = []
    for article in Article.objects.order_by("-publish_time"):        
        ar_datetime =  article.publish_time        
        date_list.append("%s-%s" % (ar_datetime.year, ar_datetime.month))
        cls_list.append(article.classification.name)        
    if archive_date:
        year = archive_date.split("-")[0]
        month = archive_date.split("-")[1]
        blogs = Article.objects.filter(publish_or_not=1, publish_time__year=year, publish_time__month=month).order_by('-publish_time')
    elif classified:
        blogs = Article.objects.filter(publish_or_not=1, classification__name=classified).order_by('-publish_time')
    else:
        blogs = Article.objects.filter(publish_or_not=1).order_by('-publish_time')
    return render_to_response('index.html', {"blogs": blogs, "date_set": set(date_list), "cls_set": set(cls_list)}, context_instance=RequestContext(request))


def blog_detail(request):
    if request.method == 'GET':
        id = request.GET.get('id', '')
        try:
            blog = Article.objects.get(id=id)
        except Article.DoesNotExist:
            raise Http404
        return render_to_response("detail.html", {"blog": blog}, context_instance=RequestContext(request))
    else:
        raise Http404


def blog_about(request):
    try:
        about_me = Resume.objects.filter(show_or_not=1)[0].content
    except:
        about_me = ""
    return render_to_response('about.html', {"about_me": about_me}, context_instance=RequestContext(request))