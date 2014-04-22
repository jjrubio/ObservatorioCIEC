from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.template.loader import get_template
from django.template import Context
from django.template.context import RequestContext
from features.models import Description
from home.models import Slider, Timeline
from staff.models import Personal_data

def home (request):
    description = Description.objects.all()
    imagenes = Slider.objects.all()
    profile = Personal_data.objects.all()
    template = 'index.html'
    return render_to_response(template, context_instance = RequestContext(request,locals()))


def timeline (request):
	events   = Timeline.objects.all()
	template = 'timeline.html'
	return render_to_response(template, context_instance = RequestContext(request,locals()))


