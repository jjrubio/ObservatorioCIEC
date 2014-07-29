import tablib
from import_export import resources
from models import Data_from_2003_4
from import_export.widgets import DecimalWidget

class Data_from_year_trimResource(resources.ModelResource, DecimalWidget):
    class Meta:
        model = Data_from_2003_4
        exclude = ('id',)
        import_id_fields = ('anio', 'trimestre', 'area', 'region_natural', 'ciudad_ind', 'fexp', 'genero', 'edad', 'etnia', 'edad_group', 'nivinst', 'anosaprob', 'pet', 'pei', 'pea', 'ocupa', 'onocla', 'oplenos', 'suboc', 'suboc1', 'suboc2', 'deso', 'deso1', 'deso2', 'deaboc1', 'deaboc2', 'sect_formal', 'sect_informal', 'sect_srvdom', 'sect_moderno', 'sect_agricola', 'sub_inv', 'sub_informal', 'ingrl', 'rama_act_1', 'rama_act_2', 'grupo_ocup_1', 'seguro', 'migracion', )
