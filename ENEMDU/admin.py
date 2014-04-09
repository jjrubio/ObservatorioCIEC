from django.contrib import admin
from models import Variable_definition, Data_from_2003_4, Data_from_2007_2


class Data_fromAdmin(admin.ModelAdmin):
    list_display = (
        'year', 'trim', 'area', 'region_natural', 'ciudad_ind',
        'fexp', 'genero', 'edad', 'etnia', 'edad_group', 'nivinst',
        'anosaprob', 'pet', 'pei', 'pea', 'ocupa', 'onocla', 'oplenos',
        'suboc', 'suboc1', 'suboc2', 'deso', 'deso1', 'deso2',
        'deaboc1', 'deaboc2', 'sect_formal', 'sect_informal',
        'sect_srvdom', 'sect_agricola', 'sub_inv', 'sub_informa',
        'ingrl', 'rama_act_1', 'rama_act_2', 'group_ocup_1', 'seguro',
        'migracion', )


admin.site.register(Variable_definition)
admin.site.register(Data_from_2003_4)
admin.site.register(Data_from_2007_2, Data_fromAdmin)
