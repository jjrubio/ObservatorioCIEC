from django.contrib import admin
from models import Slider, Timeline


class TimelineAdmin(admin.ModelAdmin):
	list_display = ('title', 'event', )


admin.site.register(Slider)
admin.site.register(Timeline, TimelineAdmin)
