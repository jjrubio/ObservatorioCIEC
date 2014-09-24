from django.shortcuts import render, render_to_response
from django.template.context import RequestContext
from django.template.loader import get_template

# Create your views here.
def comercio_page(request):
	template = 'comercio.html'
	return render_to_response(template, context_instance = RequestContext(request,locals()))