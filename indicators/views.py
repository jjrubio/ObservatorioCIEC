from django.shortcuts import HttpResponse, render, render_to_response, HttpResponseRedirect
from django.template.context import RequestContext
from models import *
import json
from django.shortcuts import get_object_or_404
from django.core import serializers


def indicator_def(request,cat_id, subcat_id, ind_id):
	json = indicators_detail(cat_id, subcat_id, ind_id)
	indicators    = Indicator.objects.all()
	subcategories = Subcategory.objects.all()
	categories    = Category.objects.all()
	template      = "indicator_def.html"
	return render_to_response(template, context_instance = RequestContext(request,locals()))

def indicators_detail(cat_id, subcat_id, ind_id):
	message = []
	subcategoriesArray =[]
	indicatorsArray =[]
	indicatorSelectArray = []

	posSubcat = int(subcat_id)
	posInd = int(ind_id)

	# if not request.is_ajax():
	subcategories = Subcategory.objects.filter(category_id = cat_id)
	indicators = Indicator.objects.filter(subcategory_id = subcategories[posSubcat-1].id)
	indicatorSelect = Indicator.objects.get(id = indicators[posInd-1].id)

	for subcat in subcategories:
		dict_subcat = {}
		dict_subcat['id'] = subcat.id
		dict_subcat['name'] = subcat.name
		dict_subcat['icon'] = subcat.icon
		subcategoriesArray.append(dict_subcat)

	for ind in indicators:
		dict_ind = {}
		dict_ind['id'] = ind.id
		dict_ind['name'] = ind.name
		dict_ind['icon'] = ind.icon
		indicatorsArray.append(dict_ind)

	dict_indSelect = {}
	dict_indSelect['id'] = indicatorSelect.id
	dict_indSelect['name'] = indicatorSelect.name
	dict_indSelect['definition'] = indicatorSelect.definition
	dict_indSelect['unit'] = indicatorSelect.unit
	dict_indSelect['formula'] = "/%s" % indicatorSelect.formula_src
	dict_indSelect['subcategory'] = ind.subcategory
	dict_indSelect['category'] = ind.subcategory.category
	indicatorSelectArray.append(dict_indSelect)

	message.append(subcategoriesArray)
	message.append(indicatorsArray)
	message.append(indicatorSelectArray)
		#data = json.dumps(message)
	return message
	# else:
	# 	return HttpResponseRedirect("/")
	# data = json.dumps(message)
	# return HttpResponse(data, content_type='application/json')

def indicator_calc(request,cat_id, subcat_id, ind_id):
	json = indicators_detail(cat_id, subcat_id, ind_id)
	# print request
	indicators    = Indicator.objects.all()
	subcategories = Subcategory.objects.all()
	categories    = Category.objects.all()
	disintegrations = Disintegration.objects.all()
	template      = "indicator_calc.html"
	return render_to_response(template, context_instance = RequestContext(request,locals()))

def list_by_no_denied(request):
	id_desagre = request.GET['id_desagregacion']
	print id_desagre
#
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

def list_desagregation(request):
	disintegrations = Disintegration.objects.all()
	data = serializers.serialize('json', disintegrations)
	#print data
	return HttpResponse(data, mimetype='application/json')

def valid(request):
	id_desagre = request.GET.getlist('id_desagregacions[]')
	id_desagre_size = len(id_desagre)
	if id_desagre_size == 0:
		data = "no hay datos"
		print data
	elif id_desagre_size == 1:
		data = "hay un dato"
		print data
	elif id_desagre_size == 2:
		data = "hay dos datos"
		print data
	#print id_desagre
	return HttpResponse(data, mimetype='application/json')

def test(request):
	test = request.GET['test']
	#data = [['2003','2004','2005'],['4.5','3.9','9.1']]
	data = ['2003', '2004', '2005']
	dato = json.dumps(data)
	return HttpResponse(dato, content_type='application/json')