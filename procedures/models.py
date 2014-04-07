from django.db import models
from indicators.models import Indicator


class Data_range(models.Model):
    start_year = models.PositiveSmallIntegerField()
    start_trim = models.PositiveSmallIntegerField()
    end_year   = models.PositiveSmallIntegerField()
    end_trim   = models.PositiveSmallIntegerField()
    indicators = models.ManyToManyField(Indicator)

    def __unicode__(self):
        return "%d-%d a %d-%d" % (self.start_year, self.start_trim, self.end_year, self.end_trim)

class Type_calc(models.Model):
	name      = models.CharField(max_length = 60)
	signature = models.CharField(max_length = 30)

