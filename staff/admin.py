from django.contrib import admin
from models import Personal_data


class Personal_dataAdmin(admin.ModelAdmin):
    list_display = ('grado_academico', 'nombre', 'apellido', 'correo', 'resumen', )


admin.site.register(Personal_data, Personal_dataAdmin)