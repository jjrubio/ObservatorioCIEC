from django.db import models


class Lista_estandares(models.Model):
    nombre = models.CharField(max_length=10)


class Paises(models.Model):
    codigo = models.PositiveSmallIntegerField(unique=True)
    pais = models.TextField()


class Periodicidad(models.Model):
    nombre = models.CharField(max_length=10)


class CGCE(models.Model):
    codigo = models.CharField(max_length=10, unique=True)
    descripcion = models.TextField()


class CIIU3(models.Model):
    codigo = models.CharField(max_length=10, unique=True)
    descripcion = models.TextField()


class CPC(models.Model):
    codigo = models.CharField(max_length=10, unique=True)
    descripcion = models.TextField()


class CUODE(models.Model):
    codigo = models.CharField(max_length=10, unique=True)
    descripcion = models.TextField()


class Nandina(models.Model):
    subpartida = models.CharField(max_length=10, unique=True)
    descripcion = models.TextField()


class Equivalencia(models.Model):
    nandina = models.ForeignKey(Nandina, to_field='subpartida')
    cpc = models.ForeignKey(CPC, to_field='codigo')
    cuode = models.ForeignKey(CUODE, to_field='codigo')
    cgce = models.ForeignKey(CGCE, to_field='codigo')
    sistema_armotizado = models.CharField(max_length=10)
    ciiu3 = models.ForeignKey(CIIU3, to_field='codigo')
    cuci3 = models.CharField(max_length=10)


class Export_CGCE(models.Model):
    ano = models.PositiveSmallIntegerField()
    mes = models.PositiveSmallIntegerField()
    pais = models.ForeignKey(Paises, to_field='codigo')
    codigo = models.ForeignKey(CGCE, to_field='codigo')
    peso = models.DecimalField(decimal_places=2, max_digits=7)
    fob = models.DecimalField(decimal_places=2, max_digits=7)


class Export_CIIU3(models.Model):
    ano = models.PositiveSmallIntegerField()
    mes = models.PositiveSmallIntegerField()
    pais = models.ForeignKey(Paises, to_field='codigo')
    codigo = models.ForeignKey(CIIU3, to_field='codigo')
    peso = models.DecimalField(decimal_places=2, max_digits=7)
    fob = models.DecimalField(decimal_places=2, max_digits=7)


class Export_CPC(models.Model):
    ano = models.PositiveSmallIntegerField()
    mes = models.PositiveSmallIntegerField()
    pais = models.ForeignKey(Paises, to_field='codigo')
    codigo = models.ForeignKey(CPC, to_field='codigo')
    peso = models.DecimalField(decimal_places=2, max_digits=7)
    fob = models.DecimalField(decimal_places=2, max_digits=7)


class Export_CUODE(models.Model):
    ano = models.PositiveSmallIntegerField()
    mes = models.PositiveSmallIntegerField()
    pais = models.ForeignKey(Paises, to_field='codigo')
    codigo = models.ForeignKey(CUODE, to_field='codigo')
    peso = models.DecimalField(decimal_places=2, max_digits=7)
    fob = models.DecimalField(decimal_places=2, max_digits=7)


class Export_Nandina(models.Model):
    ano = models.PositiveSmallIntegerField()
    mes = models.PositiveSmallIntegerField()
    pais = models.ForeignKey(Paises, to_field='codigo')
    subpartida_nandina = models.ForeignKey(Nandina, to_field='subpartida')
    peso = models.DecimalField(decimal_places=2, max_digits=7)
    fob = models.DecimalField(decimal_places=2, max_digits=7)
    subpartida_key = models.CharField(max_length=10)


class Import_CGCE(models.Model):
    ano = models.PositiveSmallIntegerField()
    mes = models.PositiveSmallIntegerField()
    pais = models.ForeignKey(Paises, to_field='codigo')
    codigo = models.ForeignKey(CGCE, to_field='codigo')
    peso = models.DecimalField(decimal_places=2, max_digits=7)
    fob = models.DecimalField(decimal_places=2, max_digits=7)
    cib = models.DecimalField(decimal_places=2, max_digits=7)


class Import_CIIU3(models.Model):
    ano = models.PositiveSmallIntegerField()
    mes = models.PositiveSmallIntegerField()
    pais = models.ForeignKey(Paises, to_field='codigo')
    codigo = models.ForeignKey(CIIU3, to_field='codigo')
    peso = models.DecimalField(decimal_places=2, max_digits=7)
    fob = models.DecimalField(decimal_places=2, max_digits=7)
    cib = models.DecimalField(decimal_places=2, max_digits=7)


class Import_CPC(models.Model):
    ano = models.PositiveSmallIntegerField()
    mes = models.PositiveSmallIntegerField()
    pais = models.ForeignKey(Paises, to_field='codigo')
    codigo = models.ForeignKey(CPC, to_field='codigo')
    peso = models.DecimalField(decimal_places=2, max_digits=7)
    fob = models.DecimalField(decimal_places=2, max_digits=7)
    cib = models.DecimalField(decimal_places=2, max_digits=7)


class Import_CUODE(models.Model):
    ano = models.PositiveSmallIntegerField()
    mes = models.PositiveSmallIntegerField()
    pais = models.ForeignKey(Paises, to_field='codigo')
    codigo = models.ForeignKey(CUODE, to_field='codigo')
    peso = models.DecimalField(decimal_places=2, max_digits=7)
    fob = models.DecimalField(decimal_places=2, max_digits=7)
    cib = models.DecimalField(decimal_places=2, max_digits=7)


class Import_Nandina(models.Model):
    ano = models.PositiveSmallIntegerField()
    mes = models.PositiveSmallIntegerField()
    pais = models.ForeignKey(Paises, to_field='codigo')
    subpartida_nandina = models.ForeignKey(Nandina, to_field='subpartida')
    peso = models.DecimalField(decimal_places=2, max_digits=7)
    fob = models.DecimalField(decimal_places=2, max_digits=7)
    cib = models.DecimalField(decimal_places=2, max_digits=7)
    subpartida_key = models.CharField(max_length=10)


class sqliteadmin_queries(models.Model):
    name = models.TextField()
    sql1 = models.TextField()