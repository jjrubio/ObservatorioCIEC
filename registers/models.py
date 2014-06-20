from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserProfile(models.Model):
	AREA_CHOICES  =  (
        ( 'E' ,   	 'Estudiante' ),
        ( 'Ing.' ,   'Ingeniero'),
        ( 'MSc.' ,   'Master'	),
        ( 'PhD.' ,   'Doctorado'),
    )
	user 			= models.OneToOneField(User)
	institution 	= models.CharField(max_length=50, default=None)
	profesion   	= models.CharField(max_length=4, choices = AREA_CHOICES , default = 'Estudiante')
	contador_visita = models.IntegerField(default=0)

	def __unicode__(self):
		return self.user.username