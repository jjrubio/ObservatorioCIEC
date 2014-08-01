from django.contrib import admin
from models import *


class BulletinAdmin(admin.ModelAdmin):
    list_display = ('body', 'pdf_src', )


class LinkAdmin(admin.ModelAdmin):
    list_display = ('title','category','url', )


class LinkCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', )


class DownloadAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'counter', 'start_date', 'end_date', )


admin.site.register(Bulletin, BulletinAdmin)
admin.site.register(Link, LinkAdmin)
admin.site.register(LinkCategory, LinkCategoryAdmin)
admin.site.register(Download, DownloadAdmin)
