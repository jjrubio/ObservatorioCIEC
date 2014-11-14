#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django import forms
from django.conf import settings

IMP_CHOICES = (('1', 'CGCE'), ('2','CIIU3'), ('3','CPC'),('4','CUODE'), ('5','NANDINA'), ('6','PAISES'), ('7','EQUIVALENCIA'), ('8','DATOS EXPORTACION'), ('9','DATOS IMPORTACION'))

class UploadFileForm(forms.Form):
	choices = forms.ChoiceField(label='Escoga que tabla desea actualizar los datos', choices=IMP_CHOICES)
	file = forms.FileField(label='Seleccione un archivo txt o csv')