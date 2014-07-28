# -*- coding: utf-8 -*-
from django.db import models


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
        verbose_name = "dato personal"
        verbose_name_plural = "Datos personales"