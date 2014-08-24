# -*- coding: utf-8 -*-
from django.db import models


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
        verbose_name = "estructura"
        verbose_name_plural = "Estructuras"

    def __unicode__(self):
        return self.represent


class Data_from_2003_4(models.Model):
    anio = models.PositiveSmallIntegerField()
    trimestre = models.PositiveSmallIntegerField()
    area = models.CharField(max_length=30, null=True)
    region_natural = models.CharField(max_length=30, null=True)
    ciudad_ind = models.CharField(max_length=30, null=True)
    fexp = models.DecimalField(decimal_places=4, max_digits=7, null=True)
    genero = models.CharField(max_length=30, null=True)
    edad = models.PositiveSmallIntegerField(null=True)
    etnia = models.CharField(max_length=30, null=True)
    edad_group = models.CharField(max_length=30, null=True)
    nivinst = models.CharField(max_length=30, null=True)
    anosaprob = models.PositiveSmallIntegerField(null=True)
    pet = models.PositiveSmallIntegerField(null=True)
    pei = models.PositiveSmallIntegerField(null=True)
    pea = models.PositiveSmallIntegerField(null=True)
    ocupa = models.PositiveSmallIntegerField(null=True)
    onocla = models.PositiveSmallIntegerField(null=True)
    oplenos = models.PositiveSmallIntegerField(null=True)
    suboc = models.PositiveSmallIntegerField(null=True)
    suboc1 = models.PositiveSmallIntegerField(null=True)
    suboc2 = models.PositiveSmallIntegerField(null=True)
    deso = models.PositiveSmallIntegerField(null=True)
    deso1 = models.PositiveSmallIntegerField(null=True)
    deso2 = models.PositiveSmallIntegerField(null=True)
    deaboc1 = models.PositiveSmallIntegerField(null=True)
    deaboc2 = models.PositiveSmallIntegerField(null=True)
    sect_formal = models.PositiveSmallIntegerField(null=True)
    sect_informal = models.PositiveSmallIntegerField(null=True)
    sect_srvdom = models.PositiveSmallIntegerField(null=True)
    sect_moderno = models.PositiveSmallIntegerField(null=True)
    sect_agricola = models.PositiveSmallIntegerField(null=True)
    sub_inv = models.PositiveSmallIntegerField(null=True)
    sub_informal = models.PositiveSmallIntegerField(null=True)
    ingrl = models.DecimalField(decimal_places=2, max_digits=7, null=True)
    rama_act_1 = models.CharField(max_length=75, null=True)
    rama_act_2 = models.CharField(max_length=75, null=True)
    grupo_ocup_1 = models.CharField(max_length=75, null=True)
    seguro = models.CharField(max_length=50, null=True)
    satis_laboral = models.PositiveSmallIntegerField(null=True)
    descon_bajos_ingresos = models.PositiveSmallIntegerField(null=True)
    descon_horarios = models.PositiveSmallIntegerField(null=True)
    descon_estabil = models.PositiveSmallIntegerField(null=True)
    descon_amb_laboral = models.PositiveSmallIntegerField(null=True)
    descon_activ = models.PositiveSmallIntegerField(null=True)
    experiencia = models.DecimalField(decimal_places=2, max_digits=5, null=True)
    migracion_extranjera = models.PositiveSmallIntegerField(null=True)
    migracion_rural_urbano = models.PositiveSmallIntegerField(null=True)
    tamano_hogar = models.DecimalField(decimal_places=2, max_digits=4, null=True)
    hogar_noFamiliar = models.PositiveSmallIntegerField(null=True)
    hogar_completo = models.PositiveSmallIntegerField(null=True)
    ingreso_hogar = models.DecimalField(decimal_places=2, max_digits=8, null=True)
    part_quehaceres = models.PositiveSmallIntegerField(null=True)
    horas_part_quehaceres = models.PositiveSmallIntegerField(null=True)
    categ_ocupa = models.CharField(max_length=75, null=True)
    condact = models.CharField(max_length=75, null=True)
    tipo_ocupa = models.CharField(max_length=75, null=True)
    tipo_deso = models.CharField(max_length=75, null=True)
    rela_jef = models.PositiveSmallIntegerField(null=True)
    analfabeta = models.PositiveSmallIntegerField(null=True)
    nocla = models.PositiveSmallIntegerField(null=True)
    ultimos_anios = models.PositiveSmallIntegerField(null=True)
    condInact = models.CharField(max_length=30, null=True)
    rentista = models.PositiveSmallIntegerField(null=True)
    jubil = models.PositiveSmallIntegerField(null=True)
    estudiant = models.PositiveSmallIntegerField(null=True)
    amaCasa = models.PositiveSmallIntegerField(null=True)
    incapacit = models.PositiveSmallIntegerField(null=True)
    otro = models.PositiveSmallIntegerField(null=True)

    class Meta:
        verbose_name = "un dato desde 2003 - 4"
        verbose_name_plural = "Datos desde 2003 - 4"


class Data_from_2007_2(models.Model):
    anio = models.PositiveSmallIntegerField()
    trimestre = models.PositiveSmallIntegerField()
    area = models.CharField(max_length=30, null=True)
    region_natural = models.CharField(max_length=30, null=True)
    ciudad_ind = models.CharField(max_length=30, null=True)
    fexp = models.DecimalField(decimal_places=4, max_digits=7, null=True)
    genero = models.CharField(max_length=30, null=True)
    edad = models.PositiveSmallIntegerField(null=True)
    etnia = models.CharField(max_length=30, null=True)
    edad_group = models.CharField(max_length=30, null=True)
    nivinst = models.CharField(max_length=30, null=True)
    anosaprob = models.PositiveSmallIntegerField(null=True)
    pet = models.PositiveSmallIntegerField(null=True)
    pei = models.PositiveSmallIntegerField(null=True)
    pea = models.PositiveSmallIntegerField(null=True)
    ocupa = models.PositiveSmallIntegerField(null=True)
    onocla = models.PositiveSmallIntegerField(null=True)
    oplenos = models.PositiveSmallIntegerField(null=True)
    suboc = models.PositiveSmallIntegerField(null=True)
    suboc1 = models.PositiveSmallIntegerField(null=True)
    suboc2 = models.PositiveSmallIntegerField(null=True)
    deso = models.PositiveSmallIntegerField(null=True)
    deso1 = models.PositiveSmallIntegerField(null=True)
    deso2 = models.PositiveSmallIntegerField(null=True)
    deaboc1 = models.PositiveSmallIntegerField(null=True)
    deaboc2 = models.PositiveSmallIntegerField(null=True)
    sect_formal = models.PositiveSmallIntegerField(null=True)
    sect_informal = models.PositiveSmallIntegerField(null=True)
    sect_srvdom = models.PositiveSmallIntegerField(null=True)
    sect_moderno = models.PositiveSmallIntegerField(null=True)
    sect_agricola = models.PositiveSmallIntegerField(null=True)
    sub_inv = models.PositiveSmallIntegerField(null=True)
    sub_informal = models.PositiveSmallIntegerField(null=True)
    ingrl = models.DecimalField(decimal_places=2, max_digits=7, null=True)
    rama_act_1 = models.CharField(max_length=75, null=True)
    rama_act_2 = models.CharField(max_length=75, null=True)
    grupo_ocup_1 = models.CharField(max_length=75, null=True)
    seguro = models.CharField(max_length=50, null=True)
    satis_laboral = models.PositiveSmallIntegerField(null=True)
    descon_bajos_ingresos = models.PositiveSmallIntegerField(null=True)
    descon_horarios = models.PositiveSmallIntegerField(null=True)
    descon_estabil = models.PositiveSmallIntegerField(null=True)
    descon_amb_laboral = models.PositiveSmallIntegerField(null=True)
    descon_activ = models.PositiveSmallIntegerField(null=True)
    experiencia = models.DecimalField(decimal_places=2, max_digits=5, null=True)
    migracion_extranjera = models.PositiveSmallIntegerField(null=True)
    migracion_rural_urbano = models.PositiveSmallIntegerField(null=True)
    tamano_hogar = models.DecimalField(decimal_places=2, max_digits=4, null=True)
    hogar_noFamiliar = models.PositiveSmallIntegerField(null=True)
    hogar_completo = models.PositiveSmallIntegerField(null=True)
    ingreso_hogar = models.DecimalField(decimal_places=2, max_digits=8, null=True)
    part_quehaceres = models.PositiveSmallIntegerField(null=True)
    horas_part_quehaceres = models.PositiveSmallIntegerField(null=True)
    categ_ocupa = models.CharField(max_length=75, null=True)
    condact = models.CharField(max_length=75, null=True)
    tipo_ocupa = models.CharField(max_length=75, null=True)
    tipo_deso = models.CharField(max_length=75, null=True)
    rela_jef = models.PositiveSmallIntegerField(null=True)
    analfabeta = models.PositiveSmallIntegerField(null=True)
    nocla = models.PositiveSmallIntegerField(null=True)
    ultimos_anios = models.PositiveSmallIntegerField(null=True)
    condInact = models.CharField(max_length=30, null=True)
    rentista = models.PositiveSmallIntegerField(null=True)
    jubil = models.PositiveSmallIntegerField(null=True)
    estudiant = models.PositiveSmallIntegerField(null=True)
    amaCasa = models.PositiveSmallIntegerField(null=True)
    incapacit = models.PositiveSmallIntegerField(null=True)
    otro = models.PositiveSmallIntegerField(null=True)

    class Meta:
        verbose_name = "un dato desde 2007 - 2"
        verbose_name_plural = "Datos desde 2007 - 2"