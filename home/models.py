from django.db import models


class Slider(models.Model):
    img_src = models.ImageField(upload_to='sliders/')


class Timeline(models.Model):
	COLOR_CHOICES  =  (
        ( 'danger' ,  'rojo' ),
        ( 'success' ,  'verde' ),
        ( 'primary' ,  'azul' ),
        ( 'warning' ,  'naranja' ),
        ( 'info' ,  'celeste' ),
    )
	title      = models.CharField(max_length=50)
	event      = models.TextField()
	icon       = models.CharField(max_length=50)
	icon_color = models.CharField(max_length=10, choices = COLOR_CHOICES, default = 'verde')

	def __unicode__(self):
		return self.title