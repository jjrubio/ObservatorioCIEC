# -*- coding: utf-8 -*-
from django.db import models


class Disintegration(models.Model):
    name = models.CharField(max_length=50, verbose_name='Nombre')

    class Meta:
        verbose_name = "desagregación"
        verbose_name_plural = 'Desagregaciones'

    def __unicode__(self):
        return self.name


class Type(models.Model):
    name           = models.CharField(max_length=50, verbose_name='Nombre')
    disintegration = models.ForeignKey(Disintegration, verbose_name='Desagregación')

    class Meta:
        verbose_name = "tipo"
        verbose_name_plural = 'Tipos'

    def __unicode__(self):
        return self.name