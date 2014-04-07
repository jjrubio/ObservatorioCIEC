from django.db import models


class Description(models.Model):
    detail = models.CharField(max_length=200)

    def __unicode__(self):
        return self.detail