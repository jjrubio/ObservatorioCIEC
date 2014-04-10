from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.template.loader import get_template
from django.template import Context
from django.template.context import RequestContext
from features.models import Description
from home.models import Slider

# Create your views here.
def home (request):
	description = Description.objects.all()
	imagenes = Slider.objects.all()
	template = "index.html"
	return render_to_response(template, context_instance = RequestContext(request,locals()))
