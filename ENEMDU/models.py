from django.db import models
from disintegrations.models import Type

class Variable_definition(models.Model):
    name        = models.CharField(max_length=50)
    description = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name


class Data_from_2003_4(models.Model):
    AREA_CHOICES = (
        ( 'R' , 'Rural'),
        ( 'U' , 'Urbano'),
    year           = models.PositiveSmallIntegerField()
    trim           = models.PositiveSmallIntegerField()
    area           = models.CharField(max_length = 1 , choices = AREA_CHOICES , default = 'Urbano')
    region_natural = models.CharField(Type, to_field='disintegration'==1)
    ciudad_ind     = models.CharField(Type, to_field='disintegration'==2)
    fexp           = models.DecimalField(max_digits=8, decimal_places=4)
    genero         = models.CharField(Type, to_field='disintegration'==3)
    edad           = models.PositiveSmallIntegerField()
    etnia          = models.CharField(Type, to_field='disintegration'==4)
    edad_group     = models.CharField(Type, to_field='disintegration'==5)
    nivinst        = models.CharField(Type, to_field='disintegration'==6)
    anosaprob      = models.PositiveSmallIntegerField()
    pet            = models.BooleanField()
    pei            = models.BooleanField()
    pea            = models.BooleanField()
    ocupa          = models.BooleanField()
    onocla         = models.BooleanField()
    oplenos        = models.BooleanField()
    suboc          = models.BooleanField()
    suboc1         = models.BooleanField()
    suboc2         = models.BooleanField()
    deso           = models.BooleanField()
    deso1          = models.BooleanField()
    deso2          = models.BooleanField()
    deaboc1        = models.BooleanField()
    deaboc2        = models.BooleanField()
    sect_formal    = models.BooleanField()
    sect_informal  = models.BooleanField()
    sect_srvdom    = models.BooleanField()
    sect_agricola  = models.BooleanField()
    sub_inv        = models.BooleanField()
    sub_informa    = models.BooleanField()
    ingrl          = models.PositiveIntegerField()
    rama_act_1     = models.CharField(max_length=75)
    rama_act_2     = models.CharField(Type, to_field='disintegration'==9)
    group_ocup_1   = models.CharField(Type, to_field='disintegration'==8)
    seguro         = models.CharField(Type, to_field='disintegration'==7)
    migracion      = models.BooleanField()


class Data_from_2007_2(models.Model):
    AREA_CHOICES = (
        ( 'R' , 'Rural'),
        ( 'U' , 'Urbano'),
    year           = models.PositiveSmallIntegerField()
    trim           = models.PositiveSmallIntegerField()
    area           = models.CharField(max_length = 1 , choices = AREA_CHOICES , default = 'Urbano')
    region_natural = models.CharField(Type, to_field='disintegration'==1)
    ciudad_ind     = models.CharField(Type, to_field='disintegration'==2)
    fexp           = models.DecimalField(max_digits=8, decimal_places=4)
    genero         = models.CharField(Type, to_field='disintegration'==3)
    edad           = models.PositiveSmallIntegerField()
    etnia          = models.CharField(Type, to_field='disintegration'==4)
    edad_group     = models.CharField(Type, to_field='disintegration'==5)
    nivinst        = models.CharField(Type, to_field='disintegration'==6)
    anosaprob      = models.PositiveSmallIntegerField()
    pet            = models.BooleanField()
    pei            = models.BooleanField()
    pea            = models.BooleanField()
    ocupa          = models.BooleanField()
    onocla         = models.BooleanField()
    oplenos        = models.BooleanField()
    suboc          = models.BooleanField()
    suboc1         = models.BooleanField()
    suboc2         = models.BooleanField()
    deso           = models.BooleanField()
    deso1          = models.BooleanField()
    deso2          = models.BooleanField()
    deaboc1        = models.BooleanField()
    deaboc2        = models.BooleanField()
    sect_formal    = models.BooleanField()
    sect_informal  = models.BooleanField()
    sect_srvdom    = models.BooleanField()
    sect_agricola  = models.BooleanField()
    sub_inv        = models.BooleanField()
    sub_informa    = models.BooleanField()
    ingrl          = models.PositiveIntegerField()
    rama_act_1     = models.CharField(max_length=75)
    rama_act_2     = models.CharField(Type, to_field='disintegration'==9)
    group_ocup_1   = models.CharField(Type, to_field='disintegration'==8)
    seguro         = models.CharField(Type, to_field='disintegration'==7)
    migracion      = models.BooleanField()