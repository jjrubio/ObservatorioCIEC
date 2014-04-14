from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.template.loader import get_template
from django.template import Context
from django.template.context import RequestContext
from features.models import Description
from home.models import Slider


def home (request):
    description = Description.objects.all()
    imagenes = Slider.objects.all()
    template = 'index.html'
    return render_to_response(template, context_instance = RequestContext(request,locals()))


def userhome (request):
    template = "userhome.html"
    return render_to_response(template, context_instance = RequestContext(request,locals()))

