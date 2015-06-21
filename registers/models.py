# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    AREA_CHOICES  =  (
        ( 'Est' ,        'Estudiante' ),
        ( 'Lic.' ,   'Licenciado'),
        ( 'Ing.' ,   'Ingeniero'),
        ( 'MSc.' ,   'Master'),
        ( 'PhD.' ,   'Doctor'),
    )
    user = models.OneToOneField(User, verbose_name='Usuario')
    institution = models.CharField(max_length=50, null=False, verbose_name='Institución')
    grado_academico = models.CharField(max_length=4, choices = AREA_CHOICES , default = 'Estudiante', verbose_name='Grado académico')
    contador_visita = models.IntegerField(default=0, verbose_name='Contador de visitas')
    telefono = models.CharField(max_length=20, null=False, verbose_name='Teléfono')
    direccion = models.CharField(max_length=100, null=False, verbose_name='Dirección')
    required_css_class = 'required'
    activation_key = models.CharField(max_length=40)
    key_expires = models.DateTimeField()

    class Meta:
        db_table = "registers_userprofile"
        verbose_name = "perfil de usuario"
        verbose_name_plural = "Perfiles de usuario"

    def __unicode__(self):
        return u'%s %s - %s' % (self.user.first_name, self.user.last_name, self.user.username)
