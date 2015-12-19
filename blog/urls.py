__author__ = 'sj_gao'
from django.conf.urls import patterns, url
import views

urlpatterns = patterns("",
                       url(r"^$", views.blog_list, name="blog_list"),
                       url(r"^article$", views.blog_list),
                       url(r'^detail/$', views.blog_detail, name="blog_detail"),
                       url(r'^about/$', views.blog_about, name="blog_about"),
                       )