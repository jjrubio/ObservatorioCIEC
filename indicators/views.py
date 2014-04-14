from django.shortcuts import render
from models import *


def calc(request):
    indicators = Indicator.objects.all()
    categories = Category.objects.all()
    template   = "form.html"
    return render(request, template, locals())
