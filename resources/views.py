# -*- coding: utf-8 -*-
from django.shortcuts import HttpResponse, render, render_to_response, HttpResponseRedirect
from django.template.context import RequestContext
from models import *
from django.shortcuts import get_object_or_404

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