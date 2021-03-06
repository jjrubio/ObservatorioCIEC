# -*- coding: utf-8 -*-
from django.db import models

                                                
class Paises(models.Model):
    codigo = models.PositiveSmallIntegerField()
    pais = models.TextField()

    class Meta:
        db_table = "comercio_paises"
        verbose_name = "país"
        verbose_name_plural = 'Paises'

    def __unicode__(self):
        return self.pais


class CGCE(models.Model):
    codigo = models.CharField(max_length=10)
    descripcion = models.TextField()

    class Meta:
        db_table = "comercio_cgce"
        verbose_name = "cgce"
        verbose_name_plural = 'CGCE'

    def __unicode__(self):
        return self.descripcion


class CIIU3(models.Model):
    codigo = models.CharField(max_length=10)
    descripcion = models.TextField()

    class Meta:
        db_table = "comercio_ciiu3"
        verbose_name = "ciiu3"
        verbose_name_plural = 'CIIU3'

    def __unicode__(self):
        return self.descripcion


class CPC(models.Model):
    codigo = models.CharField(max_length=10)
    descripcion = models.TextField()

    class Meta:
        db_table = "comercio_cpc"
        verbose_name = "cpc"
        verbose_name_plural = 'CPC'

    def __unicode__(self):
        return self.descripcion


class CUODE(models.Model):
    codigo = models.CharField(max_length=10)
    descripcion = models.TextField()

    class Meta:
        db_table = "comercio_cuode"
        verbose_name = "cuode"
        verbose_name_plural = 'CUODE'

    def __unicode__(self):
        return self.descripcion


class NANDINA(models.Model):
    subpartida = models.CharField(max_length=8)
    descripcion = models.TextField()

    class Meta:
        db_table = "comercio_nandina"
        verbose_name = "nandina"
        verbose_name_plural = 'NANDINA'

    def __unicode__(self):
        return self.descripcion


class Equivalencia(models.Model):
    nandina = models.CharField(max_length=10)
    cpc = models.CharField(max_length=10)
    cuode = models.CharField(max_length=10)
    cgce = models.CharField(max_length=10)
    sistema_armotizado = models.CharField(max_length=10)
    ciiu3 = models.CharField(max_length=10)
    cuci3 = models.CharField(max_length=10)

    class Meta:
        db_table = "comercio_equivalencia"
        verbose_name = "equivalencia"
        verbose_name_plural = 'Equivalencia'

    def __unicode__(self):
        return self.nandina


class Export_CGCE(models.Model):
    ano = models.PositiveSmallIntegerField()
    mes = models.PositiveSmallIntegerField()
    pais = models.PositiveSmallIntegerField()
    codigo = models.CharField(max_length=10)
    peso = models.DecimalField(decimal_places=2, max_digits=10)
    fob = models.DecimalField(decimal_places=2, max_digits=9)

    class Meta:
        db_table = "comercio_export_cgce"
        verbose_name = "exportación cgce"
        verbose_name_plural = 'Exportaciones CGCE'

    def __unicode__(self):
        return self.codigo


class Export_CIIU3(models.Model):
    ano = models.PositiveSmallIntegerField()
    mes = models.PositiveSmallIntegerField()
    pais = models.PositiveSmallIntegerField()
    codigo = models.CharField(max_length=10)
    peso = models.DecimalField(decimal_places=2, max_digits=10)
    fob = models.DecimalField(decimal_places=2, max_digits=9)

    class Meta:
        db_table = "comercio_export_ciiu3"
        verbose_name = "exportación ciiu3"
        verbose_name_plural = 'Exportaciones CIIU3'

    def __unicode__(self):
        return self.codigo


class Export_CPC(models.Model):
    ano = models.PositiveSmallIntegerField()
    mes = models.PositiveSmallIntegerField()
    pais = models.PositiveSmallIntegerField()
    codigo = models.CharField(max_length=10)
    peso = models.DecimalField(decimal_places=2, max_digits=10)
    fob = models.DecimalField(decimal_places=2, max_digits=9)

    class Meta:
        db_table = "comercio_export_cpc"
        verbose_name = "exportación cpc"
        verbose_name_plural = 'Exportaciones CPC'

    def __unicode__(self):
        return self.codigo


class Export_CUODE(models.Model):
    ano = models.PositiveSmallIntegerField()
    mes = models.PositiveSmallIntegerField()
    pais = models.PositiveSmallIntegerField()
    codigo = models.CharField(max_length=10)
    peso = models.DecimalField(decimal_places=2, max_digits=10)
    fob = models.DecimalField(decimal_places=2, max_digits=9)

    class Meta:
        db_table = "comercio_export_cuode"
        verbose_name = "exportación cuode"
        verbose_name_plural = 'Exportaciones CUODE'

    def __unicode__(self):
        return self.codigo


class Export_NANDINA(models.Model):
    ano = models.PositiveSmallIntegerField()
    mes = models.PositiveSmallIntegerField()
    pais = models.PositiveSmallIntegerField()
    subpartida_nandina = models.CharField(max_length=10)
    peso = models.DecimalField(decimal_places=2, max_digits=10)
    fob = models.DecimalField(decimal_places=2, max_digits=9)
    subpartida_key =  models.CharField(max_length=8)

    class Meta:
        db_table = "comercio_export_nandina"
        verbose_name = "exportación nandina"
        verbose_name_plural = 'Exportaciones NANDINA'

    def __unicode__(self):
        return self.subpartida_nandina


class Import_CGCE(models.Model):
    ano = models.PositiveSmallIntegerField()
    mes = models.PositiveSmallIntegerField()
    pais = models.PositiveSmallIntegerField()
    codigo = models.CharField(max_length=10)
    peso = models.DecimalField(decimal_places=2, max_digits=10)
    fob = models.DecimalField(decimal_places=2, max_digits=9)
    cif = models.DecimalField(decimal_places=2, max_digits=8)

    class Meta:
        db_table = "comercio_import_cgce"
        verbose_name = "importación cgce"
        verbose_name_plural = 'Importaciones CGCE'

    def __unicode__(self):
        return self.codigo


class Import_CIIU3(models.Model):
    ano = models.PositiveSmallIntegerField()
    mes = models.PositiveSmallIntegerField()
    pais = models.PositiveSmallIntegerField()
    codigo = models.CharField(max_length=10)
    peso = models.DecimalField(decimal_places=2, max_digits=10)
    fob = models.DecimalField(decimal_places=2, max_digits=9)
    cif = models.DecimalField(decimal_places=2, max_digits=8)

    class Meta:
        db_table = "comercio_import_ciiu3"
        verbose_name = "importación ciiu3"
        verbose_name_plural = 'Importaciones CIIU3'

    def __unicode__(self):
        return self.codigo


class Import_CPC(models.Model):
    ano = models.PositiveSmallIntegerField()
    mes = models.PositiveSmallIntegerField()
    pais = models.PositiveSmallIntegerField()
    codigo = models.CharField(max_length=10)
    peso = models.DecimalField(decimal_places=2, max_digits=10)
    fob = models.DecimalField(decimal_places=2, max_digits=9)
    cif = models.DecimalField(decimal_places=2, max_digits=8)

    class Meta:
        db_table = "comercio_import_cpc"
        verbose_name = "importación cpc"
        verbose_name_plural = 'Importaciones CPC'

    def __unicode__(self):
        return self.codigo


class Import_CUODE(models.Model):
    ano = models.PositiveSmallIntegerField()
    mes = models.PositiveSmallIntegerField()
    pais = models.PositiveSmallIntegerField()
    codigo = models.CharField(max_length=10)
    peso = models.DecimalField(decimal_places=2, max_digits=10)
    fob = models.DecimalField(decimal_places=2, max_digits=9)
    cif = models.DecimalField(decimal_places=2, max_digits=8)

    class Meta:
        db_table = "comercio_import_cuode"
        verbose_name = "importación cuode"
        verbose_name_plural = 'Importaciones CUODE'

    def __unicode__(self):
        return self.codigo


class Import_NANDINA(models.Model):
    ano = models.PositiveSmallIntegerField()
    mes = models.PositiveSmallIntegerField()
    pais = models.PositiveSmallIntegerField()
    subpartida_nandina = models.CharField(max_length=10)
    peso = models.DecimalField(decimal_places=2, max_digits=10)
    fob = models.DecimalField(decimal_places=2, max_digits=9)
    cif = models.DecimalField(decimal_places=2, max_digits=8)
    subpartida_key = models.CharField(max_length=8)

    class Meta:
        db_table = "comercio_import_nandina"
        verbose_name = "importación nandina"
        verbose_name_plural = 'Importaciones NANDINA'

    def __unicode__(self):
        return self.subpartida_nandina

class Export_Total(models.Model):
    ano = models.PositiveSmallIntegerField()
    mes = models.PositiveSmallIntegerField()
    fob = models.DecimalField(decimal_places=2, max_digits=9)
    peso = models.DecimalField(decimal_places=2, max_digits=10)

    class Meta:
        db_table = "comercio_export_total"
        verbose_name = "importación total"
        verbose_name_plural = 'Importaciones Totales'

    def __unicode__(self):
        return self.subpartida_nandina

class Import_Total(models.Model):
    ano = models.PositiveSmallIntegerField()
    mes = models.PositiveSmallIntegerField()
    fob = models.DecimalField(decimal_places=2, max_digits=9)
    peso = models.DecimalField(decimal_places=2, max_digits=10)
    cif = models.DecimalField(decimal_places=2, max_digits=10)

    class Meta:
        db_table = "comercio_import_total"
        verbose_name = "importación total"
        verbose_name_plural = 'Importaciones Totales'

    def __unicode__(self):
        return self.subpartida_nandina

class upload_csv_file(models.Model):
    upload = models.FileField(upload_to='csv/')

    class Meta:
        db_table = "comercio_upload_csv_file"
        verbose_name = "archivo subido"
        verbose_name_plural = 'Archivos subidos - Excel'

    def __unicode__(self):
        return self.upload