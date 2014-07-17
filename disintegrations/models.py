#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.db import models

# app_label = 'myapp'

class Disintegration(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        verbose_name = "desagregación"
        verbose_name_plural = 'Desagregaciones'


    def __unicode__(self):
        return self.name


class Type(models.Model):
    name           = models.CharField(max_length=50)
    disintegration = models.ForeignKey(Disintegration)

    class Meta:
        verbose_name = "tipo"
        verbose_name_plural = 'Tipos'

    def __unicode__(self):
        return self.name