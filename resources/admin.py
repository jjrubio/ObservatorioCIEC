from django.contrib import admin
from models import Bulletin, Link, Download


class BulletinAdmin(admin.ModelAdmin):
    list_display = ('title', 'content', 'indicator', 'excel_src', 'graph_src', )


class LinkAdmin(admin.ModelAdmin):
    list_display = ('title', 'url', )


class DownloadAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'counter', 'start_date', 'end_date', )


admin.site.register(Bulletin, BulletinAdmin)
admin.site.register(Link, LinkAdmin)
admin.site.register(Download, DownloadAdmin)
