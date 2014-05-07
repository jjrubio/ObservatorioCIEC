from django.shortcuts import HttpResponse, render, render_to_response, HttpResponseRedirect
from django.template.context import RequestContext
from models import *
from django.utils import simplejson
from django.shortcuts import get_object_or_404


def indicators_list(request):
	indicators    = Indicator.objects.all()
	subcategories = Subcategory.objects.all()
	categories    = Category.objects.all()
	template      = "indicators_list.html"
	return render_to_response(template, context_instance = RequestContext(request,locals()))

def indicators_detail(request, indicator_id):
	message = {"ind_name": "", "ind_definition": "", "ind_unit": "", "ind_formula": "", "ind_icon": "", "ind_subcategory": "", "subcategory_icon": "", "ind_category": "", "category_icon": "", }
	if request.is_ajax():
		indicator = get_object_or_404(Indicator, id=indicator_id)
		message['ind_name'] = indicator.name
		message['ind_definition'] = indicator.definition
		message['ind_unit'] = indicator.unit
		message['ind_formula'] = indicator.formula_src.path
		message['ind_icon'] = indicator.icon
		message['ind_subcategory'] = indicator.subcategory.name
		message['subcategory_icon'] = indicator.subcategory.icon
		message['ind_category'] = indicator.subcategory.category.name
		message['category_icon'] = indicator.subcategory.category.icon
	else:
		return HttpResponseRedirect("/")
	json = simplejson.dumps(message)
	return HttpResponse(json, mimetype='application/json')

def indicator_calc(request):
	indicators    = Indicator.objects.all()
	subcategories = Subcategory.objects.all()
	categories    = Category.objects.all()
	template      = "indicator_calc.html"
	return render_to_response(template, context_instance = RequestContext(request,locals()))

