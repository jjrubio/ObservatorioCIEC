from django.shortcuts import HttpResponse, render, render_to_response, HttpResponseRedirect
from django.template.context import RequestContext
from models import *
from disintegrations.models import *
import json
from django.shortcuts import get_object_or_404
from django.core import serializers


def indicator_def(request, cat_id='1', subcat_id='1', ind_id='1'):
    json = indicators_detail(cat_id, subcat_id, ind_id)
    indicators = Indicator.objects.all()
    subcategories = Subcategory.objects.all()
    categories = Category.objects.all()
    template = "indicator_def.html"
    return render_to_response(template, context_instance=RequestContext(request, locals()))


def indicators_detail(cat_id, subcat_id, ind_id):
    message = []
    subcategoriesArray = []
    indicatorsArray = []
    indicatorSelectArray = []

    posSubcat = int(subcat_id)
    posInd = int(ind_id)

    # if not request.is_ajax():
    subcategories = Subcategory.objects.filter(category_id=cat_id)
    indicators = Indicator.objects.filter(subcategory_id=subcategories[posSubcat - 1].id)
    indicatorSelect = Indicator.objects.get(id=indicators[posInd - 1].id)

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
    return message


def indicator_calc(request, cat_id='1', subcat_id='1', ind_id='1'):
    json = indicators_detail(cat_id, subcat_id, ind_id)
    # print request
    print cat_id
    print subcat_id
    print ind_id
    indicators = Indicator.objects.all()
    subcategories = Subcategory.objects.all()
    categories = Category.objects.all()
    disintegrations = Disintegration.objects.all()
    template = "indicator_calc.html"
    return render_to_response(template, context_instance=RequestContext(request, locals()))


def list_by_no_denied(request):
    id_desagre = request.GET['id_desagregacion']

    if id_desagre == '1' or id_desagre == '3':
        disintegrations = Disintegration.objects.all()
        data = serializers.serialize('json', disintegrations)
    elif id_desagre == '2':
        disintegrations = Disintegration.objects.exclude(
            id__in=[10, 4, 5, 6, 8])
        data = serializers.serialize('json', disintegrations)
    elif id_desagre == '4':
        disintegrations = Disintegration.objects.exclude(
            id__in=[10, 2, 5, 6, 8])
        data = serializers.serialize('json', disintegrations)
    elif id_desagre == '5':
        disintegrations = Disintegration.objects.exclude(
            id__in=[10, 2, 4, 6, 8, 9])
        data = serializers.serialize('json', disintegrations)
    elif id_desagre == '6':
        disintegrations = Disintegration.objects.exclude(
            id__in=[10, 2, 4, 5, 8, 9])
        data = serializers.serialize('json', disintegrations)
    elif id_desagre == '7':
        disintegrations = Disintegration.objects.exclude(id__in=[8])
        data = serializers.serialize('json', disintegrations)
    elif id_desagre == '8':
        disintegrations = Disintegration.objects.exclude(
            id__in=[10, 2, 4, 5, 6, 7, 9])
        data = serializers.serialize('json', disintegrations)
    elif id_desagre == '9':
        disintegrations = Disintegration.objects.exclude(id__in=[10, 5, 6, 8])
        data = serializers.serialize('json', disintegrations)
    elif id_desagre == '10':
        disintegrations = Disintegration.objects.exclude(
            id__in=[2, 4, 5, 6, 8, 9])
        data = serializers.serialize('json', disintegrations)
    elif id_desagre == '11':
        disintegrations = Disintegration.objects.exclude(id__in=[12, 13])
        data = serializers.serialize('json', disintegrations)
    elif id_desagre == '12':
        disintegrations = Disintegration.objects.exclude(id__in=[11, 13])
        data = serializers.serialize('json', disintegrations)
    elif id_desagre == '13':
        disintegrations = Disintegration.objects.exclude(id__in=[11, 12])
        data = serializers.serialize('json', disintegrations)

    return HttpResponse(data, content_type='application/json')


def list_desagregation(request):
    disintegrations = Disintegration.objects.all()
    data = serializers.serialize('json', disintegrations)

    return HttpResponse(data, content_type='application/json')

def test(request):
    test = request.GET['test']
    #data = [['2003','2004','2005'],['4.5','3.9','9.1']]
    data = ['2003', '2004', '2005']
    dato = json.dumps(data)
    return HttpResponse(dato, content_type='application/json')

def calc_result(request):
    indicator = request.GET['indicator']
    represent = request.GET['represent']
    method = request.GET['method']
    yearStart = request.GET['yearStart']
    trimStart = request.GET['trimStart']
    yearEnd = request.GET['yearEnd']
    trimEnd = request.GET['trimEnd']
    disintegrations = request.GET.getlist('disintegrations[]')

    indicator_int = int(indicator)
    method_int = int(method)
    yearStart_int = int(yearStart)
    trimStart_int = int(trimStart)
    yearEnd_int = int(yearEnd)
    trimEnd_int = int(trimEnd)

    represent_int = int(represent)
    
    disintegrations_size = len(disintegrations)

    if disintegrations_size == 0:
        opcion1 = 0
        opcion2 = 0
        respuesta = calc_segundo(indicator_int, represent_int, method_int, yearStart_int, trimStart_int, yearEnd_int, trimEnd_int, opcion1, opcion2)
    elif disintegrations_size == 1:
        opcion1 = int(disintegrations[0])
        opcion2 = 0
        respuesta = calc_segundo(indicator_int, represent_int, method_int, yearStart_int, trimStart_int, yearEnd_int, trimEnd_int, opcion1, opcion2)
    elif disintegrations_size == 2: 
        opcion1 = int(disintegrations[0])
        opcion2 = int(disintegrations[1])
        respuesta = calc_segundo(indicator_int, represent_int, method_int, yearStart_int, trimStart_int, yearEnd_int, trimEnd_int, opcion1, opcion2)

    data = [indicator, represent, method, yearStart, trimStart, yearEnd, trimEnd, disintegrations]
    message = json.dumps(data)
    return HttpResponse(message, content_type='application/json')

def calc_segundo(indicator, represent, method, yearStart, trimStart, yearEnd, trimEnd, opcion1, opcion2):

    #Validacion para Desagregaciones
    if opcion1 == 0 and opcion2 == 0:
        arreglo = 'Opcion 1 y Opcion 2 son Zero'
    elif opcion1 > 0:
        if opcion2 == 0:
            disintegrations_name_opcion_one = by_list(opcion1)
            disintegrations_type_opcion_one = Type.objects.filter(disintegration__id = opcion1)
            disintegrations_opcion_one_size = len(disintegrations_type_opcion_one)

            arreglo = 'Solo opcion2 es zero'

        else:
            disintegrations_name_opcion_one = by_list(opcion1)
            disintegrations_name_opcion_two = by_list(opcion2)
            disintegrations_type_opcion_one = Type.objects.filter(disintegration__id = opcion1)
            disintegrations_type_opcion_two = Type.objects.filter(disintegration__id = opcion2)
            disintegrations_opcion_one_size = len(disintegrations_type_opcion_one)
            disintegrations_opcion_two_size = len(disintegrations_type_opcion_two)

            arreglo = 'Ninguno es Zero'
    
    #Validacion por area o representatividad
    if represent == 1:
        print "Nacional"
    elif represent == 2:
        print "Urbano"
    elif represent == 3:
        print "Rural"

    #Validacion por cada indicador ya que tiene su propio query
    if method == 1:
        #Data_from_2003_4
        if indicator == 1:
            print "Indicator 1"
        elif indicator == 2:
            print "Indicator 2"
        elif indicator == 3:
            print "Indicator 3"
        elif indicator == 4:
            print "Indicator 4"
        elif indicator == 5:
            print "Indicator 5"
        elif indicator == 6:
            print "Indicator 6"
        elif indicator == 7:
            print "Indicator 7"
        elif indicator == 9:
            print "Indicator 9"
        elif indicator == 10:
            print "Indicator 10"
        elif indicator == 11:
            print "Indicator 11"
        elif indicator == 12:
            print "Indicator 12"
        elif indicator == 14:
            print "Indicator 14"
        elif indicator == 15:
            print "Indicator 15"
        elif indicator == 16:
            print "Indicator 16"
        elif indicator == 17:
            print "Indicator 17"
        elif indicator == 18:
            print "Indicator 18"
        elif indicator == 19:
            print "Indicator 19"
        elif indicator == 22:
            print "Indicator 22"
        elif indicator == 23:
            print "Indicator 23"
        elif indicator == 24:
            print "Indicator 24"
        elif indicator == 25:
            print "Indicator 25"
        elif indicator == 26:
            print "Indicator 26"
        elif indicator == 28:
            print "Indicator 28"
        elif indicator == 29:
            print "Indicator 29"
        elif indicator == 30:
            print "Indicator 30"
        elif indicator == 31:
            print "Indicator 31"
        elif indicator == 32:
            print "Indicator 32"
        elif indicator == 33:
            print "Indicator 33"
        elif indicator == 34:
            print "Indicator 34"
        elif indicator == 35:
            print "Indicator 35"
        elif indicator == 36:
            print "Indicator 36"
        elif indicator == 37:
            print "Indicator 37"
    else:
        #Data_from_2007_2
        if indicator == 1:
            print "Indicator 1"
        elif indicator == 2:
            print "Indicator 2"
        elif indicator == 3:
            print "Indicator 3"
        elif indicator == 4:
            print "Indicator 4"
        elif indicator == 5:
            print "Indicator 5"
        elif indicator == 6:
            print "Indicator 6"
        elif indicator == 7:
            print "Indicator 7"
        elif indicator == 8:
            print "Indicator 8"
        elif indicator == 9:
            print "Indicator 9"
        elif indicator == 10:
            print "Indicator 10"
        elif indicator == 11:
            print "Indicator 11"
        elif indicator == 12:
            print "Indicator 12"
        elif indicator == 13:
            print "Indicator 13"
        elif indicator == 19:
            print "Indicator 19"
        elif indicator == 20:
            print "Indicator 20"
        elif indicator == 21:
            print "Indicator 21"
        elif indicator == 22:
            print "Indicator 22"
        elif indicator == 23:
            print "Indicator 23"
        elif indicator == 24:
            print "Indicator 24"
        elif indicator == 25:
            print "Indicator 25"
        elif indicator == 26:
            print "Indicator 26"
        elif indicator == 27:
            print "Indicator 27"
        elif indicator == 28:
            print "Indicator 28"
        elif indicator == 29:
            print "Indicator 29"
        elif indicator == 30:
            print "Indicator 30"
        elif indicator == 31:
            print "Indicator 31"
        elif indicator == 32:
            print "Indicator 32"
        elif indicator == 33:
            print "Indicator 33"
        elif indicator == 34:
            print "Indicator 34"
        elif indicator == 35:
            print "Indicator 35"
        elif indicator == 36:
            print "Indicator 36"
        elif indicator == 37:
            print "Indicator 37"
        elif indicator == 38:
            print "Indicator 38"
        elif indicator == 39:
            print "Indicator 39"
        elif indicator == 40:
            print "Indicator 40"
        elif indicator == 41:
            print "Indicator 41"
        elif indicator == 42:
            print "Indicator 42"
    
    return arreglo

def by_list(id_desagregation):
    if id_desagregation == 1:
        result = 'region_natural'
    elif id_desagregation == 2:
        result = 'ciudad_ind'
    elif id_desagregation == 3:
        result = 'genero'
    elif id_desagregation == 4:
        result = 'etnia'
    elif id_desagregation == 5:
        result = 'edad_grupo'
    elif id_desagregation == 6:
        result = 'nivinst'
    elif id_desagregation == 7:
        result = 'seguro'
    elif id_desagregation == 8:
        result = 'grupo_ocup_1'
    elif id_desagregation == 9:
        result = 'rama_act_2'
    elif id_desagregation == 10:
        result = 'categ_ocupa'
    elif id_desagregation == 11:
        result = 'condact'
    elif id_desagregation == 12:
        result = 'tipo_ocupa'
    elif id_desagregation == 13:
        result = 'tipo_deso'
    return result
