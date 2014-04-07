from django.contrib import admin
from models import Indicator, Category


class IndicadorAdmin(admin.ModelAdmin):
    list_display = ('name','definition','unit','formula_src','category', )
    filter_horizontal = ('disintegrations',)


admin.site.register(Indicator, IndicadorAdmin)
admin.site.register(Category)
