from django.conf.urls import patterns, url
import views

urlpatterns = patterns("",
                       url(r"^$", views.index, name="index"),
                       url(r"^searchCmd/(?P<cmd>\w+)/$", views.cmd_tutorial_page),
                       )