# -*- coding: utf-8 -*-
from django.db import models

class string_with_title(str):
	def __new__(cls, value, title):
		instance = str.__new__(cls, value)
		instance._title = title
		return instance
																
	def title(self):
			return self._title
														 
	__copy__ = lambda self: self
	__deepcopy__ = lambda self, memodict: self


class Structure(models.Model):
	TRIM_CHOICES  =  (
		( 1 , 1 ),
		( 2 , 2 ),
		( 3 , 3 ),
		( 4,  4 ),
	)
	REPRESENT_CHOICES  =  (
		( 'Nacional' ,  'Nacional' ),
		( 'Urbana' ,  'Urbana' ),
		( 'Rural' ,  'Rural' ),
	)
	anio = models.PositiveSmallIntegerField(verbose_name='Año')
	trim = models.PositiveSmallIntegerField(choices = TRIM_CHOICES, default = 1, verbose_name='Trimestre')
	represent = models.CharField(max_length=30, choices = REPRESENT_CHOICES, default = 'Nacional', verbose_name='Representatividad', null=True)

	class Meta:
		app_label = string_with_title("ENEMDU", "ENEMDU (Indicadores) - Datos")
		db_table = "enemdu_structure"
		verbose_name = "estructura"
		verbose_name_plural = "Estructuras"

		def __unicode__(self):
			return self.represent


class Data_from_2003_4(models.Model):
	fexp = models.DecimalField(decimal_places=5, max_digits=8, null=True)
	upm = models.CharField(max_length=15, null=True, blank=True)
	dominio = models.CharField(max_length=30, null=True, blank=True)
	dominio2 = models.CharField(max_length=30, null=True, blank=True)
	anio = models.PositiveSmallIntegerField(null=True, blank=True)
	trimestre = models.PositiveSmallIntegerField(null=True, blank=True)
	region_natural = models.CharField(max_length=30, null=True, blank=True)
	area = models.CharField(max_length=30, null=True, blank=True)
	ciudad_ind = models.CharField(max_length=30, null=True, blank=True)
	zonaPlanificacion = models.CharField(max_length=30, null=True, blank=True)
	rela_jef = models.CharField(max_length=30, null=True, blank=True)
	hombre = models.PositiveSmallIntegerField(null=True, blank=True)
	edad = models.PositiveSmallIntegerField(null=True, blank=True)
	edad_group = models.CharField(max_length=30, null=True, blank=True)
	etnia = models.CharField(max_length=30, null=True, blank=True)
	genero = models.CharField(max_length=30, null=True, blank=True)
	nivinst = models.CharField(max_length=60, null=True, blank=True)
	anosaprob = models.CharField(max_length=5, null=True, blank=True)
	asisteClases = models.CharField(max_length=5, null=True, blank=True)
	analfabeta = models.CharField(max_length=5, null=True, blank=True)
	hablaEspaniol = models.CharField(max_length=5, null=True, blank=True)
	hablaIndigena = models.CharField(max_length=5, null=True, blank=True)
	hablaExtranjero = models.CharField(max_length=5, null=True, blank=True)
	experiencia = models.CharField(max_length=5, null=True, blank=True)
	haceDeportes = models.CharField(max_length=5, null=True, blank=True)
	horasDeportes = models.CharField(max_length=5, null=True, blank=True)
	migracion_extranjera = models.CharField(max_length=5, null=True, blank=True)
	mig_noprin_prin = models.CharField(max_length=5, null=True, blank=True)
	mig_prin_noprin = models.CharField(max_length=5, null=True, blank=True)
	mig_prin_prin = models.CharField(max_length=5, null=True, blank=True)
	mig_noprin_noprin = models.CharField(max_length=5, null=True, blank=True)
	tamano_hogar = models.PositiveSmallIntegerField(null=True, blank=True)
	hogar_noFamiliar = models.PositiveSmallIntegerField(null=True, blank=True)
	part_quehaceres = models.CharField(max_length=5, null=True, blank=True)
	horas_part_quehaceres = models.CharField(max_length=5, null=True, blank=True)
	hogar_completo = models.CharField(max_length=5, null=True, blank=True)
	ingrl = models.CharField(max_length=5, null=True, blank=True)
	ingreso_hogar = models.DecimalField(decimal_places=2, max_digits=8, null=True, blank=True)
	pobreza = models.CharField(max_length=5, null=True, blank=True)
	pobreza_extrema = models.CharField(max_length=5, null=True, blank=True)
	seguro = models.CharField(max_length=80, null=True, blank=True)
	pet = models.CharField(max_length=5, null=True, blank=True)
	pei = models.CharField(max_length=5, null=True, blank=True)
	pea = models.CharField(max_length=5, null=True, blank=True)
	empleo = models.CharField(max_length=5, null=True, blank=True)
	desempleo = models.CharField(max_length=5, null=True, blank=True)
	cesantes = models.CharField(max_length=5, null=True, blank=True)
	desm_nuevo = models.CharField(max_length=5, null=True, blank=True)
	semanas_busc_trab = models.CharField(max_length=5, null=True, blank=True)
	desoNoBusca = models.CharField(max_length=5, null=True, blank=True)
	grupo_ocup_1 = models.CharField(max_length=100, null=True, blank=True)
	rama_act_2 = models.CharField(max_length=100, null=True, blank=True)
	sect_informal = models.CharField(max_length=5, null=True, blank=True)
	sect_srvdom = models.CharField(max_length=5, null=True, blank=True)
	categ_ocupa = models.CharField(max_length=100, null=True, blank=True)
	tipo_deso = models.CharField(max_length=5, null=True, blank=True)
	condInact = models.CharField(max_length=5, null=True, blank=True)
	rentista = models.CharField(max_length=5, null=True, blank=True)
	jubil = models.CharField(max_length=5, null=True, blank=True)
	estudiant = models.CharField(max_length=5, null=True, blank=True)
	amaCasa = models.CharField(max_length=5, null=True, blank=True)
	incapacit = models.CharField(max_length=5, null=True, blank=True)
	otro = models.CharField(max_length=5, null=True, blank=True)
	jefeHogar = models.PositiveSmallIntegerField(null=True, blank=True)
	oplenos = models.CharField(max_length=5, null=True, blank=True)
	suboc = models.CharField(max_length=5, null=True, blank=True)
	suboc1 = models.CharField(max_length=5, null=True, blank=True)
	condact = models.CharField(max_length=75, null=True, blank=True)
	tipo_ocupa = models.CharField(max_length=75, null=True, blank=True)
	satis_laboral = models.CharField(max_length=5, null=True, blank=True)
	descon_bajos_ingresos = models.CharField(max_length=5, null=True, blank=True)
	descon_horarios = models.CharField(max_length=5, null=True, blank=True)
	descon_estabil = models.CharField(max_length=5, null=True, blank=True)
	descon_amb_laboral = models.CharField(max_length=5, null=True, blank=True)
	descon_activ = models.CharField(max_length=5, null=True, blank=True)
	sect_formal = models.CharField(max_length=5, null=True, blank=True)
	nocla_sector = models.CharField(max_length=5, null=True, blank=True)
	desemab = models.CharField(max_length=5, null=True, blank=True)
	desemoc = models.CharField(max_length=5, null=True, blank=True)
	suboc2 = models.CharField(max_length=5, null=True, blank=True)
	sub_informal = models.CharField(max_length=5, null=True, blank=True)
	sect_moderno = models.CharField(max_length=5, null=True, blank=True)
	sect_agricola = models.CharField(max_length=5, null=True, blank=True)
	sub_inv = models.CharField(max_length=5, null=True, blank=True)
	empleoAdecuado = models.CharField(max_length=5, null=True, blank=True)
	empleoInadecuado = models.CharField(max_length=5, null=True, blank=True)
	subempleo = models.CharField(max_length=5, null=True, blank=True)
	subempleoXhoras = models.CharField(max_length=5, null=True, blank=True)
	subempleoXingreso = models.CharField(max_length=5, null=True, blank=True)
	otroEmpleoInadec = models.CharField(max_length=5, null=True, blank=True)
	empleoNoclasificado = models.CharField(max_length=5, null=True, blank=True)
	empleoNoremunerado = models.CharField(max_length=5, null=True, blank=True)
	tipoEmpleo = models.CharField(max_length=5, null=True, blank=True)
	tipoEmpleoDesag = models.CharField(max_length=5, null=True, blank=True)
	sectorEmpleo = models.CharField(max_length=5, null=True, blank=True)
			
	class Meta:
		app_label = string_with_title("ENEMDU", "ENEMDU (Indicadores) - Datos")
		db_table = "enemdu_data_from_2003_4"
		verbose_name = "un dato desde 2003 - 4"
		verbose_name_plural = "Datos desde 2003 - 4"


class Data_from_2007_2(models.Model):
	fexp = models.DecimalField(decimal_places=5, max_digits=8, null=True)
	upm = models.CharField(max_length=15, null=True, blank=True)
	dominio = models.CharField(max_length=30, null=True, blank=True)
	dominio2 = models.CharField(max_length=30, null=True, blank=True)
	anio = models.PositiveSmallIntegerField(null=True, blank=True)
	trimestre = models.PositiveSmallIntegerField(null=True, blank=True)
	region_natural = models.CharField(max_length=30, null=True, blank=True)
	area = models.CharField(max_length=30, null=True, blank=True)
	ciudad_ind = models.CharField(max_length=30, null=True, blank=True)
	zonaPlanificacion = models.CharField(max_length=30, null=True, blank=True)
	rela_jef = models.CharField(max_length=30, null=True, blank=True)
	hombre = models.PositiveSmallIntegerField(null=True, blank=True)
	edad = models.PositiveSmallIntegerField(null=True, blank=True)
	edad_group = models.CharField(max_length=30, null=True, blank=True)
	etnia = models.CharField(max_length=30, null=True, blank=True)
	genero = models.CharField(max_length=30, null=True, blank=True)
	nivinst = models.CharField(max_length=60, null=True, blank=True)
	anosaprob = models.CharField(max_length=5, null=True, blank=True)
	asisteClases = models.CharField(max_length=5, null=True, blank=True)
	analfabeta = models.CharField(max_length=5, null=True, blank=True)
	hablaEspaniol = models.CharField(max_length=5, null=True, blank=True)
	hablaIndigena = models.CharField(max_length=5, null=True, blank=True)
	hablaExtranjero = models.CharField(max_length=5, null=True, blank=True)
	experiencia = models.CharField(max_length=5, null=True, blank=True)
	haceDeportes = models.CharField(max_length=5, null=True, blank=True)
	horasDeportes = models.CharField(max_length=5, null=True, blank=True)
	migracion_extranjera = models.CharField(max_length=5, null=True, blank=True)
	mig_noprin_prin = models.CharField(max_length=5, null=True, blank=True)
	mig_prin_noprin = models.CharField(max_length=5, null=True, blank=True)
	mig_prin_prin = models.CharField(max_length=5, null=True, blank=True)
	mig_noprin_noprin = models.CharField(max_length=5, null=True, blank=True)
	tamano_hogar = models.PositiveSmallIntegerField(null=True, blank=True)
	hogar_noFamiliar = models.PositiveSmallIntegerField(null=True, blank=True)
	part_quehaceres = models.CharField(max_length=5, null=True, blank=True)
	horas_part_quehaceres = models.CharField(max_length=5, null=True, blank=True)
	hogar_completo = models.CharField(max_length=5, null=True, blank=True)
	ingrl = models.CharField(max_length=5, null=True, blank=True)
	ingreso_hogar = models.DecimalField(decimal_places=2, max_digits=8, null=True, blank=True)
	pobreza = models.CharField(max_length=5, null=True, blank=True)
	pobreza_extrema = models.CharField(max_length=5, null=True, blank=True)
	seguro = models.CharField(max_length=80, null=True, blank=True)
	pet = models.CharField(max_length=5, null=True, blank=True)
	pei = models.CharField(max_length=5, null=True, blank=True)
	pea = models.CharField(max_length=5, null=True, blank=True)
	empleo = models.CharField(max_length=5, null=True, blank=True)
	desempleo = models.CharField(max_length=5, null=True, blank=True)
	cesantes = models.CharField(max_length=5, null=True, blank=True)
	desm_nuevo = models.CharField(max_length=5, null=True, blank=True)
	semanas_busc_trab = models.CharField(max_length=5, null=True, blank=True)
	desoNoBusca = models.CharField(max_length=5, null=True, blank=True)
	grupo_ocup_1 = models.CharField(max_length=100, null=True, blank=True)
	rama_act_2 = models.CharField(max_length=100, null=True, blank=True)
	sect_informal = models.CharField(max_length=5, null=True, blank=True)
	sect_srvdom = models.CharField(max_length=5, null=True, blank=True)
	categ_ocupa = models.CharField(max_length=100, null=True, blank=True)
	tipo_deso = models.CharField(max_length=5, null=True, blank=True)
	condInact = models.CharField(max_length=5, null=True, blank=True)
	rentista = models.CharField(max_length=5, null=True, blank=True)
	jubil = models.CharField(max_length=5, null=True, blank=True)
	estudiant = models.CharField(max_length=5, null=True, blank=True)
	amaCasa = models.CharField(max_length=5, null=True, blank=True)
	incapacit = models.CharField(max_length=5, null=True, blank=True)
	otro = models.CharField(max_length=5, null=True, blank=True)
	jefeHogar = models.PositiveSmallIntegerField(null=True, blank=True)
	oplenos = models.CharField(max_length=5, null=True, blank=True)
	suboc = models.CharField(max_length=5, null=True, blank=True)
	suboc1 = models.CharField(max_length=5, null=True, blank=True)
	condact = models.CharField(max_length=75, null=True, blank=True)
	tipo_ocupa = models.CharField(max_length=75, null=True, blank=True)
	satis_laboral = models.CharField(max_length=5, null=True, blank=True)
	descon_bajos_ingresos = models.CharField(max_length=5, null=True, blank=True)
	descon_horarios = models.CharField(max_length=5, null=True, blank=True)
	descon_estabil = models.CharField(max_length=5, null=True, blank=True)
	descon_amb_laboral = models.CharField(max_length=5, null=True, blank=True)
	descon_activ = models.CharField(max_length=5, null=True, blank=True)
	sect_formal = models.CharField(max_length=5, null=True, blank=True)
	nocla_sector = models.CharField(max_length=5, null=True, blank=True)
	desemab = models.CharField(max_length=5, null=True, blank=True)
	desemoc = models.CharField(max_length=5, null=True, blank=True)
	suboc2 = models.CharField(max_length=5, null=True, blank=True)
	sub_informal = models.CharField(max_length=5, null=True, blank=True)
	sect_moderno = models.CharField(max_length=5, null=True, blank=True)
	sect_agricola = models.CharField(max_length=5, null=True, blank=True)
	sub_inv = models.CharField(max_length=5, null=True, blank=True)
	empleoAdecuado = models.CharField(max_length=5, null=True, blank=True)
	empleoInadecuado = models.CharField(max_length=5, null=True, blank=True)
	subempleo = models.CharField(max_length=5, null=True, blank=True)
	subempleoXhoras = models.CharField(max_length=5, null=True, blank=True)
	subempleoXingreso = models.CharField(max_length=5, null=True, blank=True)
	otroEmpleoInadec = models.CharField(max_length=5, null=True, blank=True)
	empleoNoclasificado = models.CharField(max_length=5, null=True, blank=True)
	empleoNoremunerado = models.CharField(max_length=5, null=True, blank=True)
	tipoEmpleo = models.CharField(max_length=5, null=True, blank=True)
	tipoEmpleoDesag = models.CharField(max_length=5, null=True, blank=True)
	sectorEmpleo = models.CharField(max_length=5, null=True, blank=True)

	class Meta:
		app_label = string_with_title("ENEMDU", "ENEMDU (Indicadores) - Datos")
		db_table = "enemdu_data_from_2007_2"
		verbose_name = "un dato desde 2007 - 2"
		verbose_name_plural = "Datos desde 2007 - 2"


class upload_csv_file(models.Model):
	upload = models.FileField(upload_to='csv/')

	class Meta:
		app_label = string_with_title("ENEMDU", "ENEMDU (Indicadores) - Datos")
		db_table = "enemdu_upload_csv_file"
		verbose_name = "archivo subido txt/csv"
		verbose_name_plural = 'Archivos subidos txt/csv'

		def __unicode__(self):
			return self.name
