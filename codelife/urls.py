from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # url(r'^$', 'codelife.views.home', name='home'),
    url(r'^$', 'blog.views.blog_list', name='home'),
    url(r'^blog/', include('blog.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^comments/', include('django.contrib.comments.urls')),
    url(r'^ueditor/', include('DjangoUeditor.urls')),
    url(r'^wechat/', include('wechat.urls')),
)
