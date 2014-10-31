from django.db import models


class Lista_estandares(models.Model):
    nombre = models.CharField(max_length=10)


class Paises(models.Model):
    codigo = models.PositiveSmallIntegerField()
    pais = models.TextField()


class Periodicidad(models.Model):
    nombre = models.CharField(max_length=10)


class CGCE(models.Model):
    codigo = models.CharField(max_length=10)
    descripcion = models.TextField()


class CIIU3(models.Model):
    codigo = models.CharField(max_length=10)
    descripcion = models.TextField()


class CPC(models.Model):
    codigo = models.CharField(max_length=10)
    descripcion = models.TextField()


class CUODE(models.Model):
    codigo = models.CharField(max_length=10)
    descripcion = models.TextField()


class NANDINA(models.Model):
    subpartida = models.CharField(max_length=10)
    descripcion = models.TextField()


class Equivalencia(models.Model):
    nandina = models.CharField(max_length=10)
    cpc = models.CharField(max_length=10)
    cuode = models.CharField(max_length=10)
    cgce = models.CharField(max_length=10)
    sistema_armotizado = models.CharField(max_length=10)
    ciiu3 = models.CharField(max_length=10)
    cuci3 = models.CharField(max_length=10)


class Export_CGCE(models.Model):
    ano = models.PositiveSmallIntegerField()
    mes = models.PositiveSmallIntegerField()
    pais = models.PositiveSmallIntegerField()
    codigo = models.CharField(max_length=10)
    peso = models.DecimalField(decimal_places=2, max_digits=7)
    fob = models.DecimalField(decimal_places=2, max_digits=7)


class Export_CIIU3(models.Model):
    ano = models.PositiveSmallIntegerField()
    mes = models.PositiveSmallIntegerField()
    pais = models.PositiveSmallIntegerField()
    codigo = models.CharField(max_length=10)
    peso = models.DecimalField(decimal_places=2, max_digits=7)
    fob = models.DecimalField(decimal_places=2, max_digits=7)


class Export_CPC(models.Model):
    ano = models.PositiveSmallIntegerField()
    mes = models.PositiveSmallIntegerField()
    pais = models.PositiveSmallIntegerField()
    codigo = models.CharField(max_length=10)
    peso = models.DecimalField(decimal_places=2, max_digits=7)
    fob = models.DecimalField(decimal_places=2, max_digits=7)


class Export_CUODE(models.Model):
    ano = models.PositiveSmallIntegerField()
    mes = models.PositiveSmallIntegerField()
    pais = models.PositiveSmallIntegerField()
    codigo = models.CharField(max_length=10)
    peso = models.DecimalField(decimal_places=2, max_digits=7)
    fob = models.DecimalField(decimal_places=2, max_digits=7)


class Export_NANDINA(models.Model):
    ano = models.PositiveSmallIntegerField()
    mes = models.PositiveSmallIntegerField()
    pais = models.CharField(max_length=10)
    subpartida_nandina = models.CharField(max_length=10)
    peso = models.DecimalField(decimal_places=2, max_digits=7)
    fob = models.DecimalField(decimal_places=2, max_digits=7)
    subpartida_key =  models.CharField(max_length=10)


class Import_CGCE(models.Model):
    ano = models.PositiveSmallIntegerField()
    mes = models.PositiveSmallIntegerField()
    pais = models.PositiveSmallIntegerField()
    codigo = models.CharField(max_length=10)
    peso = models.DecimalField(decimal_places=2, max_digits=7)
    fob = models.DecimalField(decimal_places=2, max_digits=7)
    cib = models.DecimalField(decimal_places=2, max_digits=7)


class Import_CIIU3(models.Model):
    ano = models.PositiveSmallIntegerField()
    mes = models.PositiveSmallIntegerField()
    pais = models.PositiveSmallIntegerField()
    codigo = models.CharField(max_length=10)
    peso = models.DecimalField(decimal_places=2, max_digits=7)
    fob = models.DecimalField(decimal_places=2, max_digits=7)
    cib = models.DecimalField(decimal_places=2, max_digits=7)


class Import_CPC(models.Model):
    ano = models.PositiveSmallIntegerField()
    mes = models.PositiveSmallIntegerField()
    pais = models.PositiveSmallIntegerField()
    codigo = models.CharField(max_length=10)
    peso = models.DecimalField(decimal_places=2, max_digits=7)
    fob = models.DecimalField(decimal_places=2, max_digits=7)
    cib = models.DecimalField(decimal_places=2, max_digits=7)


class Import_CUODE(models.Model):
    ano = models.PositiveSmallIntegerField()
    mes = models.PositiveSmallIntegerField()
    pais = models.PositiveSmallIntegerField()
    codigo = models.CharField(max_length=10)
    peso = models.DecimalField(decimal_places=2, max_digits=7)
    fob = models.DecimalField(decimal_places=2, max_digits=7)
    cib = models.DecimalField(decimal_places=2, max_digits=7)


class Import_NANDINA(models.Model):
    ano = models.PositiveSmallIntegerField()
    mes = models.PositiveSmallIntegerField()
    pais = models.PositiveSmallIntegerField()
    subpartida_nandina = models.CharField(max_length=10)
    peso = models.DecimalField(decimal_places=2, max_digits=7)
    fob = models.DecimalField(decimal_places=2, max_digits=7)
    cib = models.DecimalField(decimal_places=2, max_digits=7)
    subpartida_key = models.CharField(max_length=10)


class sqliteadmin_queries(models.Model):
    name = models.TextField()
    sql1 = models.TextField()