# -*- coding: utf-8 -*-
from django.db import models

class string_with_title(str):
    def __new__(cls, value, title):
        instance = str.__new__(cls, value)
        instance._title = title
        return instance
    def title(self):
        return self._title
        
    __copy__ = lambda self: self
    __deepcopy__ = lambda self, memodict: self
    
class Personal_data(models.Model):
    GRADO_ACADEMICO_CHOOSE  =  (
        ( 'Ing.' ,   'Ingeniero'),
        ( 'MSc.' ,   'Master'   ),
        ( 'PhD.' ,   'Doctor'),
        ( 'Econ.' ,  'Economista'),
    )

    nombre = models.CharField(max_length=50, verbose_name='Nombre')
    apellido = models.CharField(max_length=50, verbose_name='Apellido')
    grado_academico = models.CharField(max_length=5, choices = GRADO_ACADEMICO_CHOOSE , default = 'Economista' , verbose_name='Grado académico')
    correo = models.EmailField(verbose_name='Correo')
    resumen = models.TextField(verbose_name='Resumen')

    class Meta:
        app_label = string_with_title("equipo", "Equipo de Trabajo")
        db_table = "staff_personal_data"
        verbose_name = "dato personal"
        verbose_name_plural = "Datos personales"