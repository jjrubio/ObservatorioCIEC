from django.db import models


class Variable_definition(models.Model):
    name = models.CharField(max_length=50)

    def __unicode__(self):
        return self.name


class Data_from_2003_4(models.Model):
    GENERO_CHOICES  =  (
        ( 'H' ,  'Hombre' ),
        ( 'M' ,  'Mujer' ),
    )
    year           = models.PositiveSmallIntegerField()
    trim           = models.PositiveSmallIntegerField()
    area           = models.CharField(max_length=10)
    region_natural = models.CharField(max_length=10)
    ciudad_ind     = models.CharField(max_length=15)
    fexp           = models.DecimalField(max_digits=8, decimal_places=4)
    genero         = models.CharField ( max_length = 1 , choices = GENERO_CHOICES , default = 'Hombre')
    edad           = models.PositiveSmallIntegerField()
    etnia          = models.CharField(max_length=15)
    edad_group     = models.CharField(max_length=15)
    nivinst        = models.CharField(max_length=25)
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
    rama_act_2     = models.CharField(max_length=75)
    group_ocup_1   = models.CharField(max_length=75)
    seguro         = models.CharField(max_length=25)
    migracion      = models.BooleanField()


class Data_from_2007_2(models.Model):
    GENERO_CHOICES  =  (
        ( 'H' ,  'Hombre' ),
        ( 'M' ,  'Mujer' ),
    )
    year           = models.PositiveSmallIntegerField()
    trim           = models.PositiveSmallIntegerField()
    area           = models.CharField(max_length=10)
    region_natural = models.CharField(max_length=10)
    ciudad_ind     = models.CharField(max_length=15)
    fexp           = models.DecimalField(max_digits=8, decimal_places=4)
    genero         = models.CharField ( max_length = 1 , choices = GENERO_CHOICES , default = 'Hombre')
    edad           = models.PositiveSmallIntegerField()
    etnia          = models.CharField(max_length=15)
    edad_group     = models.CharField(max_length=15)
    nivinst        = models.CharField(max_length=25)
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
    rama_act_2     = models.CharField(max_length=75)
    group_ocup_1   = models.CharField(max_length=75)
    seguro         = models.CharField(max_length=25)
    migracion      = models.BooleanField()