#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django import forms
from django.contrib.auth.models import User
from registers.models import UserProfile

class UserForm(forms.Form):
    first_name = forms.CharField(label="Nombre", widget=forms.TextInput(), required=True)
    last_name = forms.CharField(label="Apellido", widget=forms.TextInput(), required=True)
    email = forms.EmailField(label="Correo Electrónico", widget=forms.TextInput(), required=True)
    password_one = forms.CharField(label="Contraseña", widget=forms.PasswordInput(render_value=False))
    password_two = forms.CharField(label="Confirmar contraseña", widget=forms.PasswordInput(render_value=False))

    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            u = User.objects.get(username=email)
        except User.DoesNotExist:
            return email
        raise forms.ValidationError('Correo Electronico ya registrado')

    def clean_password_two(self):
        password_one = self.cleaned_data['password_one']
        password_two = self.cleaned_data['password_two']
        if password_one == password_two:
            pass
        else:
            raise forms.ValidationError('Password no coinciden')


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('institution', 'telefono', 'direccion', 'grado_academico',)

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        self.fields['institution'].label = "Institución"
        self.fields['telefono'].label = "Teléfono"
        self.fields['direccion'].label = "Dirección"
        self.fields['grado_academico'].label = "Grado académico"
        self.fields['grado_academico'].widget.attrs.update({'class' : 'selectpicker show-menu-arrow', 'data-width' : "26%"})