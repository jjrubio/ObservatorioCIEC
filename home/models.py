from django.db import models


class Slider(models.Model):
    img_src = models.ImageField(upload_to='static/sliders/')


class Timeline(models.Model):
    title = models.CharField(max_length=50)
    event = models.TextField()

    def __unicode__(self):
        return self.title