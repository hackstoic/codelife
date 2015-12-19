from django.contrib import admin

from wechat.models import *
# Register your models here.


class ImageTextAdmin(admin.ModelAdmin):
    list_display = ("title",)


class MessageAdmin(admin.ModelAdmin):
    list_display = ("context", "add_time")


class LinuxCmdAdmin(admin.ModelAdmin):
    list_display = ("name", "url")

admin.site.register(ImageText, ImageTextAdmin)
admin.site.register(Tag)
admin.site.register(Response)
admin.site.register(Message, MessageAdmin)
admin.site.register(LinuxCmd, LinuxCmdAdmin)
admin.site.register(Setting)