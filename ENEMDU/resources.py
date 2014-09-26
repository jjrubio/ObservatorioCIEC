import tablib
from import_export import resources
from models import Data_from_2003_4
from import_export import fields
from import_export import widgets
from import_export.widgets import DecimalWidget, ManyToManyWidget

class Data_from_year_trimResource(resources.ModelResource, DecimalWidget):
    class Meta:
        model = Data_from_2003_4
        exclude = ('id',)
        import_id_fields = ('anio', 'trimestre', 'area', 'region_natural', 'ciudad_ind',
        'fexp', 'genero', 'edad', 'etnia', 'edad_group', 'nivinst',
        'anosaprob', 'pet', 'pei', 'pea', 'ocupa', 'onocla', 'oplenos',
        'suboc', 'suboc1', 'suboc2', 'deso', 'deso1', 'deso2', 'deaboc1',
        'deaboc2', 'sect_formal', 'sect_informal', 'sect_srvdom',
        'sect_moderno', 'sect_agricola', 'sub_inv', 'sub_informal',
        'ingrl', 'rama_act_1', 'rama_act_2', 'grupo_ocup_1', 'seguro',
        'satis_laboral', 'descon_bajos_ingresos', 'descon_horarios',
        'descon_estabil', 'descon_amb_laboral', 'descon_activ',
        'experiencia', 'migracion_extranjera', 'migracion_rural_urbano',
        'tamano_hogar', 'hogar_noFamiliar', 'hogar_completo',
        'ingreso_hogar', 'part_quehaceres', 'horas_part_quehaceres',
        'categ_ocupa', 'condact', 'tipo_ocupa', 'tipo_deso', 'rela_jef',
        'analfabeta', 'nocla', 'ultimos_anios', 'condInact', 'rentista',
        'jubil', 'estudiant', 'amaCasa', 'incapacit', 'otro', )

