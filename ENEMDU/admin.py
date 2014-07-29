from django.contrib import admin
from models import Data_from_2003_4, Data_from_2007_2
from resources import Data_from_year_trimResource
from import_export.admin import ImportExportModelAdmin

class Data_from_year_trimAdmin(ImportExportModelAdmin):
    list_display = (
        'anio', 'trimestre', 'area', 'region_natural', 'ciudad_ind',
        'fexp', 'genero', 'edad', 'etnia', 'edad_group', 'nivinst',
        'anosaprob', 'pet', 'pei', 'pea', 'ocupa', 'onocla', 'oplenos',
        'suboc', 'suboc1', 'suboc2', 'deso', 'deso1', 'deso2',
        'deaboc1', 'deaboc2', 'sect_formal', 'sect_informal',
        'sect_srvdom', 'sect_moderno', 'sect_agricola', 'sub_inv', 'sub_informal',
        'ingrl', 'rama_act_1', 'rama_act_2', 'grupo_ocup_1', 'seguro',
        'migracion', )
    resource_class = Data_from_year_trimResource
    pass



admin.site.register(Data_from_2003_4, Data_from_year_trimAdmin)
admin.site.register(Data_from_2007_2, Data_from_year_trimAdmin)
