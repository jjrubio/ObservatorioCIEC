from django.db import models
from disintegrations.models import Disintegration

class Category(models.Model):
    name = models.CharField(max_length=50)
    icon = models.CharField(max_length=20)

    def __unicode__(self):
        return self.name


class Subcategory(models.Model):
    name     = models.CharField(max_length=50)
    icon = models.CharField(max_length=20)
    category = models.ForeignKey(Category)

    def __unicode__(self):
        return self.name

class Indicator(models.Model):
    name            = models.CharField(max_length=75)
    definition      = models.TextField()
    unit            = models.CharField(max_length=10)
    formula_src     = models.ImageField(upload_to='formulas/')
    icon = models.CharField(max_length=20)
    subcategory     = models.ForeignKey(Subcategory)
    disintegrations = models.ManyToManyField(Disintegration)

    def __unicode__(self):
        return self.name

