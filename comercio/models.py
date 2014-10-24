from django.db import models

# Create your models here.

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

class EQUIVALENCIA(models.Model):
	NANDINA = models.CharField(max_length=10)
	CPC = models.CharField(max_length=10)
	CUODE = models.CharField(max_length=10)
	CGCE = models.CharField(max_length=10)
	SISTEMA_ARMONIZADO = models.CharField(max_length=10)
	CIIU3 = models.CharField(max_length=10)
	CUCI3 = models.CharField(max_length=10)

class EXPORT_CGCE(models.Model):
	ano = models.PositiveSmallIntegerField()
	mes = models.PositiveSmallIntegerField()
	pais = models.PositiveSmallIntegerField()
	codigo = models.CharField(max_length=10)
	peso = models.DecimalField(decimal_places=2, max_digits=4)
	fob = models.DecimalField(decimal_places=2, max_digits=4)

class EXPORT_CIIU3(models.Model):
	ano = models.PositiveSmallIntegerField()
	mes = models.PositiveSmallIntegerField()
	pais = models.PositiveSmallIntegerField()
	codigo = models.CharField(max_length=10)
	peso = models.DecimalField(decimal_places=2, max_digits=4)
	fob = models.DecimalField(decimal_places=2, max_digits=4)

class EXPORT_CPC(models.Model):
	ano = models.PositiveSmallIntegerField()
	mes = models.PositiveSmallIntegerField()
	pais = models.PositiveSmallIntegerField()
	codigo = models.CharField(max_length=10)
	peso = models.DecimalField(decimal_places=2, max_digits=4)
	fob = models.DecimalField(decimal_places=2, max_digits=4)

class CUODE(models.Model):
	ano = models.PositiveSmallIntegerField()
	mes = models.PositiveSmallIntegerField()
	pais = models.PositiveSmallIntegerField()
	codigo = models.CharField(max_length=10)
	peso = models.DecimalField(decimal_places=2, max_digits=4)
	fob = models.DecimalField(decimal_places=2, max_digits=4)

class NANDINA(models.Model):
	ano = models.PositiveSmallIntegerField()
	mes = models.PositiveSmallIntegerField()
	pais = models.PositiveSmallIntegerField()
	subpartida_nandina = models.CharField(max_length=10)
	peso = models.DecimalField(decimal_places=2, max_digits=4)
	fob = models.DecimalField(decimal_places=2, max_digits=4)
	subpartida_key = models.CharField(max_length=10)

class IMPORT_CGCE(models.Model):
	ano = models.PositiveSmallIntegerField()
	mes = models.PositiveSmallIntegerField()
	pais = models.PositiveSmallIntegerField()
	codigo = models.CharField(max_length=10)
	peso = models.DecimalField(decimal_places=2, max_digits=4)
	fob = models.DecimalField(decimal_places=2, max_digits=4)
	cib = models.DecimalField(decimal_places=2, max_digits=4)

class IMPORT_CIIU3(models.Model):
	ano = models.PositiveSmallIntegerField()
	mes = models.PositiveSmallIntegerField()
	pais = models.PositiveSmallIntegerField()
	codigo = models.CharField(max_length=10)
	peso = models.DecimalField(decimal_places=2, max_digits=4)
	fob = models.DecimalField(decimal_places=2, max_digits=4)
	cib = models.DecimalField(decimal_places=2, max_digits=4)

class IMPORT_CPC(models.Model):
	ano = models.PositiveSmallIntegerField()
	mes = models.PositiveSmallIntegerField()
	pais = models.PositiveSmallIntegerField()
	codigo = models.CharField(max_length=10)
	peso = models.DecimalField(decimal_places=2, max_digits=4)
	fob = models.DecimalField(decimal_places=2, max_digits=4)
	cib = models.DecimalField(decimal_places=2, max_digits=4)

class IMPORT_CUODE(models.Model):
	ano = models.PositiveSmallIntegerField()
	mes = models.PositiveSmallIntegerField()
	pais = models.PositiveSmallIntegerField()
	codigo = models.CharField(max_length=10)
	peso = models.DecimalField(decimal_places=2, max_digits=4)
	fob = models.DecimalField(decimal_places=2, max_digits=4)
	cib = models.DecimalField(decimal_places=2, max_digits=4)

class IMPORT_NANDINA(models.Model):
	ano = models.PositiveSmallIntegerField()
	mes = models.PositiveSmallIntegerField()
	pais = models.PositiveSmallIntegerField()
	subpartida_nandina = models.CharField(max_length=10)
	peso = models.DecimalField(decimal_places=2, max_digits=4)
	fob = models.DecimalField(decimal_places=2, max_digits=4)
	cib = models.DecimalField(decimal_places=2, max_digits=4)
	subpartida_key = models.CharField(max_length=10)

class LISTA_ESTANDARES(models.Model):
	nombre = models.CharField(max_length=10)

class NANDINA(models.Model):
	subpartida = models.CharField(max_length=10)
	descripcion = models.TextField()

class PAISES(models.Model):
	codigo = models.PositiveSmallIntegerField()
	pais = models.TextField()

class PERIODICIDAD(models.Model):
	nombre = models.CharField(max_length=10)

class SQLITEADMIN_QUERIES(models.Model):
	name = models.TextField()
	SQL1 = models.TextField()