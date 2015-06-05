# -*- coding: utf-8 -*-
from django.db import models
from disintegrations.models import Disintegration


class string_with_title(str):
    def __new__(cls, value, title):
        instance = str.__new__(cls, value)
        instance._title = title
        return instance
                                
    def title(self):
        return self._title

    __copy__ = lambda self: self
    __deepcopy__ = lambda self, memodict: self


class Category(models.Model):
    name = models.CharField(max_length=50, verbose_name='Nombre')
    icon = models.CharField(max_length=20, verbose_name='Nombre del ícono')

    class Meta:
        verbose_name = "categoría"
        verbose_name_plural = "Categorías"
        db_table = "indicators_category"

    def __unicode__(self):
        return self.name


class Subcategory(models.Model):
    name = models.CharField(max_length=50, verbose_name='Nombre')
    icon = models.CharField(max_length=20, verbose_name='Nombre del ícono')
    category = models.ForeignKey(Category, verbose_name='Categoría')

    class Meta:
        db_table = 'indicators_subcategory'
        verbose_name = "subcategoría"
        verbose_name_plural = "Subcategorías"

    def __unicode__(self):
        return self.name


class Indicator(models.Model):
    name = models.CharField(max_length=75, verbose_name='Nombre')
    definition = models.TextField(verbose_name='Definición')
    unit = models.CharField(max_length=10, verbose_name='Unidad')
    formula_src = models.ImageField(upload_to='formulas/', verbose_name='Imagen fórmula')
    icon = models.CharField(max_length=20, verbose_name='Nombre del ícono')
    subcategory = models.ForeignKey(Subcategory, verbose_name='Subcategoría')
    counter = models.PositiveIntegerField(verbose_name='# de veces calculada')

    class Meta:
        db_table = 'indicators_indicator'
        verbose_name = "indicador"
        verbose_name_plural = "Indicadores"
        ordering = ["-counter"]

    def __unicode__(self):
        return self.name


class Method(models.Model):
    fecha_1 = models.CharField(max_length=15, verbose_name='Fecha 1')
    fecha_2 = models.CharField(max_length=15, verbose_name='Fecha 2')
    description = models.TextField(verbose_name='Descripción')
    indicator = models.ManyToManyField(Indicator, through='Metodologia_Indicator')

    class Meta:
        verbose_name = "Metodología"
        verbose_name_plural = "Metodologías"

class Metodologia_Indicator(models.Model):
    method = models.ForeignKey(Method)
    indicator = models.ForeignKey(Indicator)
    disintegration = models.ForeignKey(Disintegration)