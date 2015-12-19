from django.contrib import admin
from blog.models import *
# Register your models here.


class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'website')
    search_fields = ('name',)


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('caption', 'subcaption', 'classification', 'publish_time', 'update_time', "publish_or_not")
    list_filter = ('publish_time',)
    date_hierarchy = 'publish_time'
    ordering = ('-publish_time',)
    filter_horizontal = ('tags',)


class ResumeAdmin(admin.ModelAdmin):
	list_display = ('name', 'last_update', 'show_or_not')

admin.site.register(Article, ArticleAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Tag)
admin.site.register(Classification)
admin.site.register(Resume, ResumeAdmin)