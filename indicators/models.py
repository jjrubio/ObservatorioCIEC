from django.db import models
from disintegrations.models import Disintegration


class Category(models.Model):
    name = models.CharField(max_length=50)

    def __unicode__(self):
        return self.name


class Subcategory(models.Model):
    name     = models.CharField(max_length=50)
    category = models.ForeignKey(Category)

    def __unicode__(self):
        return self.name


class Indicator(models.Model):
    name            = models.CharField(max_length=75)
    definition      = models.TextField()
    unit            = models.CharField(max_length=10)
    formula_src     = models.ImageField(upload_to='indicators/static/formulas/')
    subcategory     = models.ForeignKey(Subcategory)
    disintegrations = models.ManyToManyField(Disintegration)

    def __unicode__(self):
        return self.name

