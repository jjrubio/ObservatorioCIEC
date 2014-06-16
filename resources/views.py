from django.shortcuts import HttpResponse, render, render_to_response, HttpResponseRedirect
from django.template.context import RequestContext
from models import *
from django.utils import simplejson
from django.shortcuts import get_object_or_404


def links(request):
    links = Link.objects.all()
    categories = LinkCategory.objects.all()
    template = "links.html"
    return render_to_response(template, context_instance = RequestContext(request,locals()))

def bulletins(request):
    links = Link.objects.all()
    categories = LinkCategory.objects.all()
    template = "bulletins.html"
    return render_to_response(template, context_instance = RequestContext(request,locals()))