from django.db import models
from disintegrations.models import Type, Disintegration

class Variable_definition(models.Model):
    name        = models.CharField(max_length=50)
    description = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name


class Data_from_2003_4(models.Model):
    AREA_CHOICES  =  (
        ( 'R' ,  'Rural' ),
        ( 'U' ,  'Urbano' ),
    )
    year           = models.PositiveSmallIntegerField()
    trim           = models.PositiveSmallIntegerField()
    area           = models.CharField( max_length = 1 , choices = AREA_CHOICES , default = 'Urbano')
    region_natural = models.ForeignKey(Type, to_field ='disintegration.id'==1, related_name='data_from_2003_4s_region_naturals')
    ciudad_ind     = models.ForeignKey(Type, to_field ='disintegration.id'==2, related_name='data_from_2003_4s_ciudad_inds')
    fexp           = models.DecimalField(max_digits=8, decimal_places=4)
    genero         = models.ForeignKey(Type, to_field ='disintegration.id'==3, related_name='data_from_2003_4s_generos')
    edad           = models.PositiveSmallIntegerField()
    etnia          = models.ForeignKey(Type, to_field='disintegration.id'==4, related_name='data_from_2003_4s_etnias')
    edad_group     = models.ForeignKey(Type, to_field='disintegration.id'==5, related_name='data_from_2003_4s_edad_groups')
    nivinst        = models.ForeignKey(Type, to_field='disintegration.id'==6, related_name='data_from_2003_4s_nivinsts')
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
    rama_act_2     = models.ForeignKey(Type, to_field='disintegration.id'==9, related_name='data_from_2003_4s_rama_act_2s')
    group_ocup_1   = models.ForeignKey(Type, to_field='disintegration.id'==8, related_name='data_from_2003_4s_group_ocup_1s')
    seguro         = models.ForeignKey(Type, to_field='disintegration.id'==7, related_name='data_from_2003_4s_migracions')
    migracion      = models.BooleanField()


class Data_from_2007_2(models.Model):
    AREA_CHOICES  =  (
        ( 'R' ,  'Rural' ),
        ( 'U' ,  'Urbano' ),
    )
    year           = models.PositiveSmallIntegerField()
    trim           = models.PositiveSmallIntegerField()
    area           = models.CharField( max_length = 1 , choices = AREA_CHOICES , default = 'Urbano')
    region_natural = models.ForeignKey(Type, to_field ='disintegration.id'==1, related_name='data_from_2007_2s_region_naturals')
    ciudad_ind     = models.ForeignKey(Type, to_field ='disintegration.id'==2, related_name='data_from_2007_2s_ciudad_inds')
    fexp           = models.DecimalField(max_digits=8, decimal_places=4)
    genero         = models.ForeignKey(Type, to_field ='disintegration.id'==3, related_name='data_from_2007_2s_generos')
    edad           = models.PositiveSmallIntegerField()
    etnia          = models.ForeignKey(Type, to_field='disintegration.id'==4, related_name='data_from_2007_2s_etnias')
    edad_group     = models.ForeignKey(Type, to_field='disintegration.id'==5, related_name='data_from_2007_2s_edad_groups')
    nivinst        = models.ForeignKey(Type, to_field='disintegration.id'==6, related_name='data_from_2007_2s_nivinsts')
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
    rama_act_2     = models.ForeignKey(Type, to_field='disintegration.id'==9, related_name='data_from_2007_2s_rama_act_2s')
    group_ocup_1   = models.ForeignKey(Type, to_field='disintegration.id'==8, related_name='data_from_2007_2s_group_ocup_1s')
    seguro         = models.ForeignKey(Type, to_field='disintegration.id'==7, related_name='data_from_2007_2s_migracions')
    migracion      = models.BooleanField()
