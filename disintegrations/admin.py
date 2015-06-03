from django.contrib import admin
from models import Disintegration, Type


class TypeAdmin(admin.ModelAdmin):
	list_display  = ('name', 'disintegration', )


admin.site.register(Disintegration)
admin.site.register(Type, TypeAdmin)
