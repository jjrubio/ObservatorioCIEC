from django.db import models


class Personal_data(models.Model):
    GRADO_ACADEMICO_CHOOSE  =  (
        ( 'Ing.' ,   'Ingeniero'),
        ( 'MSc.' ,   'Master'   ),
        ( 'PhD.' ,   'Doctor'),
        ( 'Econ.' ,  'Economista'),
    )

    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    grado_academico = models.CharField(max_length=5, choices = GRADO_ACADEMICO_CHOOSE , default = 'Economista')
    correo = models.EmailField()
    resumen = models.TextField()

    class Meta:
        verbose_name = "dato personal"
        verbose_name_plural = "Datos personales"



