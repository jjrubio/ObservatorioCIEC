from django.contrib import admin
from models import *

class TypeAdminPais(admin.ModelAdmin):
    list_display  = ('codigo', 'pais', )

class TypeAdminEstandares(admin.ModelAdmin):
    list_display  = ('codigo', 'descripcion', )

class TypeAdminNandina(admin.ModelAdmin):
    list_display  = ('subpartida', 'descripcion', )

class TypeAdminEquivalencia(admin.ModelAdmin):
    list_display  = ('nandina', 'cpc', 'cuode', 'cgce', 'sistema_armotizado', 'ciiu3', 'cuci3', )

class TypeAdminExportEstandares(admin.ModelAdmin):
    list_display  = ('ano', 'mes', 'pais', 'codigo', 'peso', 'fob', )

class TypeAdminExportNandina(admin.ModelAdmin):
    list_display  = ('ano', 'mes', 'pais', 'subpartida_nandina', 'peso', 'fob', 'subpartida_key', )

class TypeAdminImportEstandares(admin.ModelAdmin):
    list_display  = ('ano', 'mes', 'pais', 'codigo', 'peso', 'fob', 'cif', )

class TypeAdminImportNandina(admin.ModelAdmin):
    list_display  = ('ano', 'mes', 'pais', 'subpartida_nandina', 'peso', 'fob', 'cif', 'subpartida_key', )

class TypeAdminUpload(admin.ModelAdmin):
    list_display  = ('upload', )	

admin.site.register(Paises, TypeAdminPais)
admin.site.register(CGCE,TypeAdminEstandares)
admin.site.register(CIIU3,TypeAdminEstandares)
admin.site.register(CPC,TypeAdminEstandares)
admin.site.register(CUODE,TypeAdminEstandares)
admin.site.register(NANDINA,TypeAdminNandina)
admin.site.register(Equivalencia,TypeAdminEquivalencia)
admin.site.register(Export_CGCE,TypeAdminExportEstandares)
admin.site.register(Export_CIIU3,TypeAdminExportEstandares)
admin.site.register(Export_CPC,TypeAdminExportEstandares)
admin.site.register(Export_CUODE,TypeAdminExportEstandares)
admin.site.register(Export_NANDINA,TypeAdminExportNandina)
admin.site.register(Import_CGCE,TypeAdminImportEstandares)
admin.site.register(Import_CIIU3,TypeAdminImportEstandares)
admin.site.register(Import_CPC,TypeAdminImportEstandares)
admin.site.register(Import_CUODE,TypeAdminImportEstandares)
admin.site.register(Import_NANDINA,TypeAdminImportNandina)
admin.site.register(upload_csv_file,TypeAdminUpload)