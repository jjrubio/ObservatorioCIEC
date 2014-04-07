from django.contrib import admin
from models import Data_range, Type_calc


class Data_rangeAdmin(admin.ModelAdmin):
    list_display      = ('start_year', 'start_trim', 'end_year', 'end_trim', )
    filter_horizontal = ('indicators', )


class Type_calcAdmin(admin.ModelAdmin):
    list_display = ('name', 'signature', )


admin.site.register(Data_range, Data_rangeAdmin)
admin.site.register(Type_calc, Type_calcAdmin)
