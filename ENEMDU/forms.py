#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django import forms
from django.conf import settings


IMP_CHOICES = (('1', 'Datos 2003-4 a 2007-1'), ('2','Datos 2007-2 a la actualidad'))


class UploadFileForm(forms.Form):
	choices = forms.ChoiceField(label='Escoga que tabla desea cargar los datos', choices=IMP_CHOICES)
	file = forms.FileField(label='Seleccione un archivo txt o csv')