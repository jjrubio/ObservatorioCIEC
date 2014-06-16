from django.shortcuts import HttpResponse, render, render_to_response, HttpResponseRedirect
from django.template.context import RequestContext
from models import *
from django.utils import simplejson
from django.shortcuts import get_object_or_404
from django.core import serializers


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
		message['ind_formula'] = "/%s" % indicator.formula_src
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
	disintegrations = Disintegration.objects.all()
	template      = "indicator_calc.html"
	return render_to_response(template, context_instance = RequestContext(request,locals()))

def list_by_no_denied(request):
	id_desagre = request.GET['id_desagregacion']
	print id_desagre
	
	if id_desagre == '1' or id_desagre == '3':
		disintegrations = Disintegration.objects.all()
		data = serializers.serialize('json', disintegrations)
	elif id_desagre == '2':
		disintegrations = Disintegration.objects.exclude(id__in=[10,4,5,6,8])
		data = serializers.serialize('json', disintegrations)
	elif id_desagre == '4':
		disintegrations = Disintegration.objects.exclude(id__in=[10,2,5,6,8])
		data = serializers.serialize('json', disintegrations)
	elif id_desagre == '5':
		disintegrations = Disintegration.objects.exclude(id__in=[10,2,4,6,8,9])
		data = serializers.serialize('json', disintegrations)
	elif id_desagre == '6':
		disintegrations = Disintegration.objects.exclude(id__in=[10,2,4,5,8,9])
		data = serializers.serialize('json', disintegrations)
	elif id_desagre == '7':
		disintegrations = Disintegration.objects.exclude(id__in=[8])
		data = serializers.serialize('json', disintegrations)
	elif id_desagre == '8':
		disintegrations = Disintegration.objects.exclude(id__in=[10,2,4,5,6,7,9])
		data = serializers.serialize('json', disintegrations)
	elif id_desagre == '9':
		disintegrations = Disintegration.objects.exclude(id__in=[10,5,6,8])
		data = serializers.serialize('json', disintegrations)
	elif id_desagre == '10':
		disintegrations = Disintegration.objects.exclude(id__in=[2,4,5,6,8,9])
		data = serializers.serialize('json', disintegrations)
	elif id_desagre == '11':
		disintegrations = Disintegration.objects.exclude(id__in=[12,13])
		data = serializers.serialize('json', disintegrations)
	elif id_desagre == '12':
		disintegrations = Disintegration.objects.exclude(id__in=[11,13])
		data = serializers.serialize('json', disintegrations)
	elif id_desagre == '13':
		disintegrations = Disintegration.objects.exclude(id__in=[11,12])
		data = serializers.serialize('json', disintegrations)

	print data
	
	return HttpResponse(data, mimetype='application/json')