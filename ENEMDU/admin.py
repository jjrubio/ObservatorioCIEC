from django.contrib import admin
from models import *


class StructureAdmin(admin.ModelAdmin):
    list_display = ('anio', 'trim', 'represent' )


class Data_from_year_trimAdmin(admin.ModelAdmin):
    list_display = (
        'fexp','upm','dominio','dominio2','anio','trimestre',
        'region_natural','area','ciudad_ind','zonaPlanificacion',
        'rela_jef','hombre','edad','edad_group','etnia','genero','nivinst','anosaprob','asisteClases',
        'analfabeta','hablaEspaniol','hablaIndigena','hablaExtranjero','experiencia','haceDeportes','horasDeportes',
        'migracion_extranjera','mig_noprin_prin','mig_prin_noprin','mig_prin_prin','mig_noprin_noprin','tamano_hogar',
        'hogar_noFamiliar','part_quehaceres','horas_part_quehaceres','hogar_completo','ingrl','ingreso_hogar','pobreza',
        'pobreza_extrema','seguro','pet','pei','pea','empleo','desempleo','cesantes','desm_nuevo','semanas_busc_trab',
        'desoNoBusca','grupo_ocup_1','rama_act_2','sect_informal','sect_srvdom','categ_ocupa','tipo_deso','condInact',
        'rentista','jubil','estudiant','amaCasa','incapacit','otro','jefeHogar','oplenos','suboc','suboc1','condact',
        'tipo_ocupa','satis_laboral','descon_bajos_ingresos','descon_horarios','descon_estabil','descon_amb_laboral',
        'descon_activ','sect_formal','nocla_sector','desemab','desemoc','suboc2','sub_informal','sect_moderno','sect_agricola',
        'sub_inv','empleoAdecuado','empleoInadecuado','subempleo','subempleoXhoras','subempleoXingreso','otroEmpleoInadec',
        'empleoNoclasificado','empleoNoremunerado','tipoEmpleo','tipoEmpleoDesag','sectorEmpleo',
    )


class TypeAdminUpload(admin.ModelAdmin):
    list_display  = ('upload', )

admin.site.register(Structure, StructureAdmin)
admin.site.register(Data_from_2003_4, Data_from_year_trimAdmin)
admin.site.register(Data_from_2007_2, Data_from_year_trimAdmin)
admin.site.register(upload_csv_file,TypeAdminUpload)