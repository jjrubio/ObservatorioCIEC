# -*- coding: utf-8 -*-
from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.template.loader import get_template
from django.template import Context
from django.template.context import RequestContext
from features.models import Description
from home.models import Slider, Timeline
from staff.models import Personal_data
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
import time
from datetime import datetime

def slider(request):
    imagenes = Slider.objects.all()
    template = 'slider.html'

    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    fecha_now = str(datetime.now())
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    get_ip = IP.objects.filter(ip=ip)

    get_value_counter = Counter.objects.all()

    if not get_ip:
        ip_save = IP(ip=ip, fecha = fecha_now)
        ip_save.save()
        
        new_counter = get_value_counter[0].counter + 1
        save_new_counter = Counter.objects.update(counter=new_counter)
    else:
        if ( datetime.strptime(fecha_now[:-7], "%Y-%m-%d %H:%M:%S") -  datetime.strptime(get_ip[0].fecha[:-7], "%Y-%m-%d %H:%M:%S")).days > 0:
            update_ip = IP.objects.filter(ip=get_ip[0].ip).update(fecha=fecha_now)
            new_counter = get_value_counter[0].counter + 1
            save_new_counter = Counter.objects.update(counter=new_counter)

    contador = Counter.objects.all()
    return render_to_response(template, context_instance = RequestContext(request,locals()))

def map(request):
    template = 'map.html'
    return render_to_response(template, context_instance = RequestContext(request,locals()))

def contactos (request):
    template = 'contactos.html'
    return render_to_response(template, context_instance = RequestContext(request,locals()))

def timeline (request):
    events   = Timeline.objects.all()
    template = 'timeline.html'
    return render_to_response(template, context_instance = RequestContext(request,locals()))

def about(request):
    template = 'about.html'
    return render_to_response(template, context_instance = RequestContext(request,locals()))  