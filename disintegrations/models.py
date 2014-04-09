from django.db import models


class Disintegration(models.Model):
    name = models.CharField(max_length=50)

    def __unicode__(self):
        return self.name


class Type(models.Model):
    name           = models.CharField(max_length=50)
    disintegration = models.ForeignKey(Disintegration)

    def __unicode__(self):
        return self.name
