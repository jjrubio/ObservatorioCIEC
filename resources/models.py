from django.db import models


class Bulletin(models.Model):
    title     = models.CharField(max_length=50)
    content   = models.TextField()
    indicator = models.CharField(max_length=50)
    excel_src = models.FileField(upload_to='resources/static/excels/')
    graph_src = models.ImageField(upload_to='resources/static/graphs/')
    # pdf_src   = models.ImageField(upload_to='resources/static/pdfs/')


class Link(models.Model):
    title = models.CharField(max_length=100)
    url   = models.URLField()


class Download(models.Model):
    code       = models.PositiveIntegerField()
    name       = models.CharField(max_length=50)
    counter    = models.PositiveIntegerField()
    start_date = models.DateField()
    end_date   = models.DateField()