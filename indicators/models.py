from django.db import models
from disintegrations.models import Disintegration


class Category(models.Model):
    name = models.CharField(max_length=50)

    def __unicode__(self):
        return self.name


class Indicator(models.Model):
    name            = models.CharField(max_length=75)
    definition      = models.TextField()
    unit            = models.CharField(max_length=10)
    formula_src     = models.ImageField(upload_to='indicators/static/formulas/')
    category        = models.ForeignKey(Category)
    disintegrations = models.ManyToManyField(Disintegration)

    def __unicode__(self):
        return self.name

