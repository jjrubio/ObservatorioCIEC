from django.contrib import admin
from models import Indicator, Subcategory, Category


class IndicadorAdmin(admin.ModelAdmin):
    list_display = ('name','definition','unit','formula_src','counter','subcategory', )
    #filter_horizontal = ('disintegrations',)


class SubcategoryAdmin(admin.ModelAdmin):
    list_display = ('name','category', )


admin.site.register(Indicator, IndicadorAdmin)
admin.site.register(Subcategory, SubcategoryAdmin)
admin.site.register(Category)
