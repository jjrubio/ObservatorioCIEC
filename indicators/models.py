# -*- coding: utf-8 -*-
from django.db import models
from disintegrations.models import Disintegration


class Category(models.Model):
    name = models.CharField(max_length=50, verbose_name='Nombre')
    icon = models.CharField(max_length=20, verbose_name='Nombre del ícono')

    class Meta:
        verbose_name = "categoría"
        verbose_name_plural = "Categorías"

    def __unicode__(self):
        return self.name


class Subcategory(models.Model):
    name     = models.CharField(max_length=50, verbose_name='Nombre')
    icon = models.CharField(max_length=20, verbose_name='Nombre del ícono')
    category = models.ForeignKey(Category, verbose_name='Categoría')

    class Meta:
        verbose_name = "subcategoría"
        verbose_name_plural = "Subcategorías"

    def __unicode__(self):
        return self.name


class Indicator(models.Model):
    name            = models.CharField(max_length=75, verbose_name='Nombre')
    definition      = models.TextField(verbose_name='Definición')
    unit            = models.CharField(max_length=10, verbose_name='Unidad')
    formula_src     = models.ImageField(upload_to='formulas/', verbose_name='Imagen fórmula')
    icon = models.CharField(max_length=20, verbose_name='Nombre del ícono')
    subcategory     = models.ForeignKey(Subcategory, verbose_name='Subcategoría')
    disintegrations = models.ManyToManyField(Disintegration, verbose_name='Desagregaciones')

    class Meta:
        verbose_name = "indicador"
        verbose_name_plural = "Indicadores"

    def __unicode__(self):
        return self.name

