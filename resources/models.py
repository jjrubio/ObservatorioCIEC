# -*- coding: utf-8 -*-
from django.db import models
from indicators.models import Indicator

class Bulletin(models.Model):
    pdf_src = models.FileField(upload_to='pdfs/', verbose_name='Archivo de PDF')

    class Meta:
        app_label = "Recursos"
        db_table = "resources_bulletin"
        verbose_name = "boletín"
        verbose_name_plural = "Boletines"

    def __unicode__(self):
        return ("Boletin Edicion no."+unicode(self.id))


class LinkCategory(models.Model):
    name = models.CharField(max_length=50, verbose_name='Nombre')

    class Meta:
        app_label = "Recursos"
        db_table = "resources_linkcategory"
        verbose_name = "enlace externo - definición categoría"
        verbose_name_plural = "Enlaces externos - Definición Categoría"

    def __unicode__(self):
        return self.name


class Link(models.Model):
    title = models.CharField(max_length=100, verbose_name='Título')
    category = models.ForeignKey(LinkCategory, verbose_name='Categoría')
    url   = models.URLField(verbose_name='Enlace Web')

    class Meta:
        app_label = "Recursos"
        db_table = "resources_link"
        verbose_name = "enlace externo - definición enlace"
        verbose_name_plural = "Enlaces externos - Definición Enlace"

    def __unicode__(self):
        return self.title


class Download(models.Model):
    code = models.PositiveIntegerField(verbose_name='Código')
    name = models.CharField(max_length=50, verbose_name='Nombre')
    counter = models.PositiveIntegerField(verbose_name='Contador')
    start_date = models.DateField(verbose_name='Fecha inicial')
    end_date   = models.DateField(verbose_name='Fecha final')

    class Meta:
        verbose_name = "descarga"
        verbose_name_plural = "Descargas"
        db_table = 'resources_download'

    def __unicode__(self):
        return self.code

# class Ip_controller(models.Model):
#     ip = models.CharField(max_length=20, verbose_name='Dirección IP')
#     fecha_actual = models.CharField(max_length=50, verbose_name='Fecha actual', null=True, blank=True)

#     class Meta:
#         verbose_name = "Controlador de IP"
#         verbose_name_plural = "Controlador de IP's"
#         db_table = 'resources_ip_controller'

#     def __unicode__(self):
#         return self.ip