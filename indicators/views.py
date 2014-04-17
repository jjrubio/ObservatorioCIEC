from django.shortcuts import render, render_to_response
from django.template.context import RequestContext
from models import *


def calc(request):
    indicators = Indicator.objects.all()
    categories = Category.objects.all()
    template   = "form.html"
    return render(request, template, locals())

def indicators_list(request):
	indicators    = Indicator.objects.all()
	subcategories = Subcategory.objects.all()
	categories    = Category.objects.all()
	template      = "indicators_list.html"
	return render_to_response(template, context_instance = RequestContext(request,locals()))

def indicators_menu(request):
	indicators    = Indicator.objects.all()
	subcategories = Subcategory.objects.all()
	categories    = Category.objects.all()
	template      = "indicators_menu.html"
	return render(request, template, locals())
