# -*- coding: utf-8 -*-
from django.db import models
from indicators.models import Indicator
from tinymce import models as tinymce_models

class Bulletin(models.Model):
    pdf_src = models.FileField(upload_to='pdfs/', verbose_name='Archivo de PDF')

    class Meta:
        verbose_name = "boletín"
        verbose_name_plural = "Boletines"

    def __unicode__(self):
        return ("Boletin Edicion no."+unicode(self.id))


class LinkCategory(models.Model):
    name = models.CharField(max_length=50, verbose_name='Nombre')

    class Meta:
        verbose_name = "categoría de enlace"
        verbose_name_plural = "Categorías de enlaces"

    def __unicode__(self):
        return self.name


class Link(models.Model):
    title = models.CharField(max_length=100, verbose_name='Título')
    category = models.ForeignKey(LinkCategory, verbose_name='Categoría')
    url   = models.URLField(verbose_name='Enlace Web')

    class Meta:
        verbose_name = "enlace"
        verbose_name_plural = "Enlaces"

    def __unicode__(self):
        return self.title


class Download(models.Model):
    code       = models.PositiveIntegerField(verbose_name='Código')
    name       = models.CharField(max_length=50, verbose_name='Nombre')
    counter    = models.PositiveIntegerField(verbose_name='Contador')
    start_date = models.DateField(verbose_name='Fecha inicial')
    end_date   = models.DateField(verbose_name='Fecha final')

    class Meta:
        verbose_name = "descarga"
        verbose_name_plural = "Descargas"

    def __unicode__(self):
        return self.code