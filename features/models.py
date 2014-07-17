#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.db import models


class Description(models.Model):
    detail = models.CharField(max_length=200)

    class Meta:
        verbose_name = "descripción"
        verbose_name_plural = "Descripciones"

    def __unicode__(self):
        return self.detail