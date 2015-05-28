# -*- coding: utf-8 -*-
from django.db import models


class Slider(models.Model):
    img_src = models.ImageField(upload_to='sliders/', verbose_name='Imagen')

    def __unicode__(self):
        return "Imagen "+unicode(self.id)


class Timeline(models.Model):
    COLOR_CHOICES  =  (
        ( 'danger' ,  'rojo' ),
        ( 'success' ,  'verde' ),
        ( 'primary' ,  'azul' ),
        ( 'warning' ,  'naranja' ),
        ( 'info' ,  'celeste' ),
    )
    title      = models.CharField(max_length=50, verbose_name='Título')
    event      = models.TextField(verbose_name='Evento')
    icon       = models.CharField(max_length=50, verbose_name='Nombre del ícono')
    icon_color = models.CharField(max_length=10, choices = COLOR_CHOICES, default = 'verde', verbose_name='Color del ícono')

    class Meta:
        verbose_name = "suceso"
        verbose_name_plural = "Línea del tiempo"
        db_table = 'home_timeline'

    def __unicode__(self):
        return self.title