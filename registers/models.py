from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserProfile(models.Model):
	AREA_CHOICES  =  (
        ( 'Est' ,   	 'Estudiante' ),
        ( 'Ing.' ,   'Ingeniero'),
        ( 'MSc.' ,   'Master'	),
        ( 'PhD.' ,   'Doctor'   ),
        ( 'Lic.' ,   'Licenciado'),
    )
	user 			= models.OneToOneField(User)
	institution 	= models.CharField(max_length=50, null=False)
	grado_academico = models.CharField(max_length=4, choices = AREA_CHOICES , default = 'Estudiante')
	contador_visita = models.IntegerField(default=0)
	telefono = models.IntegerField(null=False)
	direccion = models.CharField(max_length=100, null=False)


	def __unicode__(self):
		return u'%s %s - %s' % (self.user.first_name, self.user.last_name, self.user.username)