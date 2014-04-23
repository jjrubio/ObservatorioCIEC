from django.contrib import admin
from models import Personal_data


class Personal_dataAdmin(admin.ModelAdmin):
    list_display = ('name', 'lastname', 'about', 'phone', 'email', 'facebook', 'twitter', 'linkedin', 'img_src')


admin.site.register(Personal_data, Personal_dataAdmin)
