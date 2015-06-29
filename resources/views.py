# -*- coding: utf-8 -*-
from django.shortcuts import HttpResponse, render, render_to_response, HttpResponseRedirect
from django.template.context import RequestContext
from models import *
from django.shortcuts import get_object_or_404
import pickle
import json
from json import JSONEncoder
from django.core import serializers


class PythonObjectEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (list, dict, str, unicode, int, float, bool, type(None))):
            return JSONEncoder.default(self, obj)
        return {'_python_object': pickle.dumps(obj)}
        
def as_python_object(dct):
    if '_python_object' in dct:
        return pickle.loads(str(dct['_python_object']))
    return dct

def links(request):
    links = Link.objects.all()
    categories = LinkCategory.objects.all()
    template = "links.html"
    return render_to_response(template, context_instance = RequestContext(request,locals()))

def bulletins(request):
    bulletins = Bulletin.objects.all()
    template = "bulletins.html"
    return render_to_response(template, context_instance = RequestContext(request,locals()))

def pdf_view(request, bulletin_id):
    bulletin = Bulletin.objects.get(id = bulletin_id)
    with open(bulletin.pdf_src.path, 'r') as pdf:
        response = HttpResponse(pdf.read(), mimetype='application/pdf')
        response['Content-Disposition'] = 'inline;filename=Observatorio_Economico_Social_Edicion_'+bulletin_id+'.pdf'
        return response
    pdf.closed

def search(request):
    data_result = []
    template = 'bulletins.html'
    text = request.GET['txt_search'].encode('ascii','ignore')
    text_int = int(text)
    bulletins_filtrados = Bulletin.objects.filter(id__contains=text_int)
    data = serializers.serialize('json', bulletins_filtrados)
    return HttpResponse(data, content_type='application/json')