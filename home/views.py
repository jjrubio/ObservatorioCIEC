from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.template.loader import get_template
from django.template import Context
from django.template.context import RequestContext
from features.models import Description
from home.models import Slider, Timeline
from staff.models import Personal_data
from registers.forms import UserAuthenticationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required

def slider(request):
    imagenes = Slider.objects.all()
    template = 'slider.html'
    return render_to_response(template, context_instance = RequestContext(request,locals()))

def map(request):
    template = 'map.html'
    return render_to_response(template, context_instance = RequestContext(request,locals()))    

def home (request):
    signin = UserAuthenticationForm(request.POST or None)
    if signin.is_valid():
        login(request, signin.get_user())

    template = 'index.html'
    return render_to_response(template, context_instance = RequestContext(request,locals()))

def timeline (request):
    events   = Timeline.objects.all()
    template = 'timeline.html'
    return render_to_response(template, context_instance = RequestContext(request,locals()))


