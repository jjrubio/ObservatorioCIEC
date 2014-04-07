from django.db import models


class Personal_data(models.Model):
    name     = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    about    = models.TextField()
    phone    = models.CharField(max_length=15)
    email    = models.EmailField()
    facebook = models.URLField()
    twitter  = models.URLField()
    linkedin = models.URLField()
