from django.shortcuts import HttpResponse, render, render_to_response, HttpResponseRedirect
from django.template.context import RequestContext
from models import *
from disintegrations.models import *
from ENEMDU.models import *
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
    represent_int = int(represent)
    method_int = int(method)
    yearStart_int = int(yearStart)
    trimStart_int = int(trimStart)
    yearEnd_int = int(yearEnd)
    trimEnd_int = int(trimEnd)

    disintegrations_size = len(disintegrations)

    #######Jeff
    if method_int == 1 :
        valor = 1
        column_1 = get_column_1(indicator_int, yearStart_int, trimStart_int, yearEnd_int, trimEnd_int)
        # print column_1
    else:
        valor = 2
    print valor
    ########

    if disintegrations_size == 0:
        opcion1 = 0
        opcion2 = 0
        # respuesta = calc_segundo(indicator_int, represent_int, method_int, yearStart_int, trimStart_int, yearEnd_int, trimEnd_int, opcion1, opcion2)
    elif disintegrations_size == 1:
        opcion1 = int(disintegrations[0])
        opcion2 = 0
        # respuesta = calc_segundo(indicator_int, represent_int, method_int, yearStart_int, trimStart_int, yearEnd_int, trimEnd_int, opcion1, opcion2)
    elif disintegrations_size == 2:
        opcion1 = int(disintegrations[0])
        opcion2 = int(disintegrations[1])
        # respuesta = calc_segundo(indicator_int, represent_int, method_int, yearStart_int, trimStart_int, yearEnd_int, trimEnd_int, opcion1, opcion2)

    #data = [indicator, represent, method, yearStart, trimStart, yearEnd, trimEnd, disintegrations]
    # data = [respuesta]
    data = [column_1]
    message = json.dumps(data)
    return HttpResponse(message, content_type='application/json')

def get_column_1(indicator_int, yearStart_int, trimStart_int, yearEnd_int, trimEnd_int):
    column = []
    trim_1 = trimStart_int
    trim_2 = 5
    for i in range(yearStart_int, yearEnd_int+1):
        print i
        if i == yearEnd_int:
            trim_2 = trimEnd_int+1

        for j in range(trim_1, trim_2):
            print j
            column = column + list(Data_from_2003_4.objects.filter(anio=i, trimestre=j).values_list("pet", flat=True))#completar method 2 y value_list
            # print len(resultado)
            if j == 4:
                trim_1 = 1
    return column

def calc_segundo(indicator, represent, method, yearStart, trimStart, yearEnd, trimEnd, opcion1, opcion2):
    resultado = []
    subquery = []

    #Validacion por area o representatividad
    if represent == 1:
        #where1 = {'area': 'Urbano'}
        where = 'Urbano'
    elif represent == 2:
        #where = {'area': 'Urbano'}
        where = 'Urbano'
    elif represent == 3:
        #where = {'area': 'Rural'}
        where = 'Rural'

    #Validacion para Desagregaciones
    if opcion1 == 0 and opcion2 == 0:
        if indicator == 1 or indicator == 2:
            subquery.append({'area':where, 'anio__range':(yearStart,yearEnd)})
        if indicator == 3 or indicator == 4 or indicator == 5:
            subquery.append({'area':where, 'anio__range':(yearStart,yearEnd),'pet':1})
        elif indicator == 6 or indicator == 7 or indicator == 9 or indicator == 10 or indicator == 11 or indicator == 12 or indicator == 13 or indicator == 14 or indicator == 15 or indicator == 16 or indicator == 17 or indicator == 18 or indicator == 19 or indicator == 20 or indicator == 21 or indicator == 22 or indicator == 23:
            subquery.append({'area':where, 'anio__range':(yearStart,yearEnd),'pea':1})
        elif indicator == 24 or indicator == 25 or indicator == 26 or indicator == 27 or indicator == 38 or indicator == 39 or indicator == 40 or indicator == 41 or indicator == 42:
            subquery.append({'area':where, 'anio__range':(yearStart,yearEnd),'ocupa':1})
        elif indicator == 32 or indicator == 33 or indicator == 34 or indicator == 35:
            subquery.append({'area':where, 'anio__range':(yearStart,yearEnd),'rela_jef':1})
    elif opcion1 > 0:
        if opcion2 == 0:
            disintegrations_name_opcion_one = by_list(opcion1)
            disintegrations_type_opcion_one = Type.objects.filter(disintegration__id = opcion1)
            disintegrations_opcion_one_size = len(disintegrations_type_opcion_one)

            for i in range(0,disintegrations_opcion_one_size):
                if indicator == 1 or indicator == 2:
                    subquery.append({disintegrations_name_opcion_one:disintegrations_type_opcion_one[i], 'area':where, 'anio__range':(yearStart,yearEnd)})
                if indicator == 3 or indicator == 4 or indicator == 5:
                    subquery.append({disintegrations_name_opcion_one:disintegrations_type_opcion_one[i], 'area':where, 'anio__range':(yearStart,yearEnd), 'pet':1})
                elif indicator == 6 or indicator == 7 or indicator == 9 or indicator == 10 or indicator == 11 or indicator == 12 or indicator == 13 or indicator == 14 or indicator == 15 or indicator == 16 or indicator == 17 or indicator == 18 or indicator == 19 or indicator == 20 or indicator == 21 or indicator == 22 or indicator == 23:
                    subquery.append({disintegrations_name_opcion_one:disintegrations_type_opcion_one[i], 'area':where, 'anio__range':(yearStart,yearEnd), 'pea':1})
                elif indicator == 24 or indicator == 25 or indicator == 26 or indicator == 27 or indicator == 38 or indicator == 39 or indicator == 40 or indicator == 41 or indicator == 42:
                    subquery.append({disintegrations_name_opcion_one:disintegrations_type_opcion_one[i], 'area':where, 'anio__range':(yearStart,yearEnd), 'ocupa':1})
                elif indicator == 32 or indicator == 33 or indicator == 34 or indicator == 35:
                    subquery.append({disintegrations_name_opcion_one:disintegrations_type_opcion_one[i], 'area':where, 'anio__range':(yearStart,yearEnd), 'rela_jef':1})

        else:
            disintegrations_name_opcion_one = by_list(opcion1)
            disintegrations_name_opcion_two = by_list(opcion2)
            disintegrations_type_opcion_one = Type.objects.filter(disintegration__id = opcion1)
            disintegrations_type_opcion_two = Type.objects.filter(disintegration__id = opcion2)
            disintegrations_opcion_one_size = len(disintegrations_type_opcion_one)
            disintegrations_opcion_two_size = len(disintegrations_type_opcion_two)

            for i in range(0,disintegrations_opcion_one_size):
                for j in range(0,disintegrations_opcion_two_size):
                    if indicator == 1 or indicator == 2:
                        subquery.append({disintegrations_name_opcion_one:disintegrations_type_opcion_one[i], disintegrations_name_opcion_two:disintegrations_type_opcion_two[j],'area':where, 'anio__range':(yearStart,yearEnd)})
                    if indicator == 3 or indicator == 4 or indicator == 5:
                        subquery.append({disintegrations_name_opcion_one:disintegrations_type_opcion_one[i], disintegrations_name_opcion_two:disintegrations_type_opcion_two[j],'area':where, 'anio__range':(yearStart,yearEnd),'pet':1})
                    elif indicator == 6 or indicator == 7 or indicator == 9 or indicator == 10 or indicator == 11 or indicator == 12 or indicator == 13 or indicator == 14 or indicator == 15 or indicator == 16 or indicator == 17 or indicator == 18 or indicator == 19 or indicator == 20 or indicator == 21 or indicator == 22 or indicator == 23:
                        subquery.append({disintegrations_name_opcion_one:disintegrations_type_opcion_one[i], disintegrations_name_opcion_two:disintegrations_type_opcion_two[j],'area':where, 'anio__range':(yearStart,yearEnd),'pea':1})
                    elif indicator == 24 or indicator == 25 or indicator == 26 or indicator == 27 or indicator == 38 or indicator == 39 or indicator == 40 or indicator == 41 or indicator == 42:
                        subquery.append({disintegrations_name_opcion_one:disintegrations_type_opcion_one[i], disintegrations_name_opcion_two:disintegrations_type_opcion_two[j],'area':where, 'anio__range':(yearStart,yearEnd),'ocupa':1})
                    elif indicator == 32 or indicator == 33 or indicator == 34 or indicator == 35:
                        subquery.append({disintegrations_name_opcion_one:disintegrations_type_opcion_one[i], disintegrations_name_opcion_two:disintegrations_type_opcion_two[j],'area':where, 'anio__range':(yearStart,yearEnd),'rela_jef':1})

    #Validacion por cada indicador ya que tiene su propio query
    if method == 1:
        #Data_from_2003_4
        if indicator == 1:
            for x in range(0,len(subquery)):
                resultado.append(Data_from_2003_4.objects.filter(**subquery[x]))
        elif indicator == 2:
            for x in range(0,len(subquery)):
                resultado.append(Data_from_2003_4.objects.filter(**subquery[x]))
        elif indicator == 3:
            for x in range(0,len(subquery)):
                resultado.append(Data_from_2003_4.objects.filter(**subquery[x]))
        elif indicator == 4:
            for x in range(0,len(subquery)):
                resultado.append(Data_from_2003_4.objects.filter(**subquery[x]))
        elif indicator == 5:
            for x in range(0,len(subquery)):
                resultado.append(Data_from_2003_4.objects.filter(**subquery[x]))
        elif indicator == 6:
            for x in range(0,len(subquery)):
                resultado.append(Data_from_2003_4.objects.filter(**subquery[x]))
        elif indicator == 7:
            for x in range(0,len(subquery)):
                resultado.append(Data_from_2003_4.objects.filter(**subquery[x]))
        elif indicator == 9:
            for x in range(0,len(subquery)):
                resultado.append(Data_from_2003_4.objects.filter(**subquery[x]))
        elif indicator == 10:
            for x in range(0,len(subquery)):
                resultado.append(Data_from_2003_4.objects.filter(**subquery[x]))
        elif indicator == 11:
            for x in range(0,len(subquery)):
                resultado.append(Data_from_2003_4.objects.filter(**subquery[x]))
        elif indicator == 12:
            for x in range(0,len(subquery)):
                resultado.append(Data_from_2003_4.objects.filter(**subquery[x]))
        elif indicator == 14:
            for x in range(0,len(subquery)):
                resultado.append(Data_from_2003_4.objects.filter(**subquery[x]))
        elif indicator == 15:
            for x in range(0,len(subquery)):
                resultado.append(Data_from_2003_4.objects.filter(**subquery[x]))
        elif indicator == 16:
            for x in range(0,len(subquery)):
                resultado.append(Data_from_2003_4.objects.filter(**subquery[x]))
        elif indicator == 17:
            for x in range(0,len(subquery)):
                resultado.append(Data_from_2003_4.objects.filter(**subquery[x]))
        elif indicator == 18:
            for x in range(0,len(subquery)):
                resultado.append(Data_from_2003_4.objects.filter(**subquery[x]))
        elif indicator == 19:
            for x in range(0,len(subquery)):
                resultado.append(Data_from_2003_4.objects.filter(**subquery[x]))
        elif indicator == 22:
            for x in range(0,len(subquery)):
                resultado.append(Data_from_2003_4.objects.filter(**subquery[x]))
        elif indicator == 23:
            for x in range(0,len(subquery)):
                resultado.append(Data_from_2003_4.objects.filter(**subquery[x]))
        elif indicator == 24:
            for x in range(0,len(subquery)):
                resultado.append(Data_from_2003_4.objects.filter(**subquery[x]))
        elif indicator == 25:
            for x in range(0,len(subquery)):
                resultado.append(Data_from_2003_4.objects.filter(**subquery[x]))
        elif indicator == 26:
            for x in range(0,len(subquery)):
                resultado.append(Data_from_2003_4.objects.filter(**subquery[x]).exclude(ingrl__isnull=True))
                #Exclude ingrl IS NULL
        elif indicator == 28:
            for x in range(0,len(subquery)):
                resultado.append(Data_from_2003_4.objects.filter(**subquery[x]).exclude(anosaprob__isnull=True))
                #Exlude anosaprob IS NULL
        elif indicator == 29:
            for x in range(0,len(subquery)):
                resultado.append(Data_from_2003_4.objects.filter(**subquery[x]).exclude(experiencia__isnull=True))
                #Exlude experiencia IS NULL
        elif indicator == 30:
            for x in range(0,len(subquery)):
                resultado.append(Data_from_2003_4.objects.filter(**subquery[x]))
        elif indicator == 31:
            for x in range(0,len(subquery)):
                resultado.append(Data_from_2003_4.objects.filter(**subquery[x]))
        elif indicator == 32:
            for x in range(0,len(subquery)):
                resultado.append(Data_from_2003_4.objects.filter(**subquery[x]))
        elif indicator == 33:
            for x in range(0,len(subquery)):
                resultado.append(Data_from_2003_4.objects.filter(**subquery[x]))
        elif indicator == 34:
            for x in range(0,len(subquery)):
                resultado.append(Data_from_2003_4.objects.filter(**subquery[x]))
        elif indicator == 35:
            for x in range(0,len(subquery)):
                resultado.append(Data_from_2003_4.objects.filter(**subquery[x]))
        elif indicator == 36:
            for x in range(0,len(subquery)):
                resultado.append(Data_from_2003_4.objects.filter(**subquery[x]))
        elif indicator == 37:
            for x in range(0,len(subquery)):
                resultado.append(Data_from_2003_4.objects.filter(**subquery[x]))
    else:
        #Data_from_2007_2
        if indicator == 1:
            for x in range(0,len(subquery)):
                resultado.append(Data_from_2007_2.objects.filter(**subquery[x]))
        elif indicator == 2:
            for x in range(0,len(subquery)):
                resultado.append(Data_from_2007_2.objects.filter(**subquery[x]))
        elif indicator == 3:
            for x in range(0,len(subquery)):
                resultado.append(Data_from_2007_2.objects.filter(**subquery[x]))
        elif indicator == 4:
            for x in range(0,len(subquery)):
                resultado.append(Data_from_2007_2.objects.filter(**subquery[x]))
        elif indicator == 5:
            for x in range(0,len(subquery)):
                resultado.append(Data_from_2007_2.objects.filter(**subquery[x]))
        elif indicator == 6:
            for x in range(0,len(subquery)):
                resultado.append(Data_from_2007_2.objects.filter(**subquery[x]))
        elif indicator == 7:
            for x in range(0,len(subquery)):
                resultado.append(Data_from_2007_2.objects.filter(**subquery[x]))
        elif indicator == 8:
            for x in range(0,len(subquery)):
                resultado.append(Data_from_2007_2.objects.filter(**subquery[x]))
        elif indicator == 9:
            for x in range(0,len(subquery)):
                resultado.append(Data_from_2007_2.objects.filter(**subquery[x]))
        elif indicator == 10:
            for x in range(0,len(subquery)):
                resultado.append(Data_from_2007_2.objects.filter(**subquery[x]))
        elif indicator == 11:
            for x in range(0,len(subquery)):
                resultado.append(Data_from_2007_2.objects.filter(**subquery[x]))
        elif indicator == 12:
            for x in range(0,len(subquery)):
                resultado.append(Data_from_2007_2.objects.filter(**subquery[x]))
        elif indicator == 13:
            for x in range(0,len(subquery)):
                resultado.append(Data_from_2007_2.objects.filter(**subquery[x]))
        elif indicator == 19:
            for x in range(0,len(subquery)):
                resultado.append(Data_from_2007_2.objects.filter(**subquery[x]))
        elif indicator == 20:
            for x in range(0,len(subquery)):
                resultado.append(Data_from_2007_2.objects.filter(**subquery[x]))
        elif indicator == 21:
            for x in range(0,len(subquery)):
                resultado.append(Data_from_2007_2.objects.filter(**subquery[x]))
        elif indicator == 22:
            for x in range(0,len(subquery)):
                resultado.append(Data_from_2007_2.objects.filter(**subquery[x]))
        elif indicator == 23:
            for x in range(0,len(subquery)):
                resultado.append(Data_from_2007_2.objects.filter(**subquery[x]))
        elif indicator == 24:
            for x in range(0,len(subquery)):
                resultado.append(Data_from_2007_2.objects.filter(**subquery[x]))
        elif indicator == 25:
            for x in range(0,len(subquery)):
                resultado.append(Data_from_2007_2.objects.filter(**subquery[x]))
        elif indicator == 26:
            for x in range(0,len(subquery)):
                resultado.append(Data_from_2007_2.objects.filter(**subquery[x]).exclude(ingrl__isnull=True))
                #Exclude ingrl IS NULL
        elif indicator == 27:
            for x in range(0,len(subquery)):
                resultado.append(Data_from_2007_2.objects.filter(**subquery[x]).exclude(satis_laboral__isnull=True))
                #Exclude satis_laboral IS NULL
        elif indicator == 28:
            for x in range(0,len(subquery)):
                resultado.append(Data_from_2007_2.objects.filter(**subquery[x]).exclude(anosaprob__isnull=True))
                #Exclude anosaprob IS NULL
        elif indicator == 29:
            for x in range(0,len(subquery)):
                resultado.append(Data_from_2007_2.objects.filter(**subquery[x]).exclude(experiencia__isnull=True))
                #Exclude experiencia IS NULL
        elif indicator == 30:
            for x in range(0,len(subquery)):
                resultado.append(Data_from_2007_2.objects.filter(**subquery[x]))
        elif indicator == 31:
            for x in range(0,len(subquery)):
                resultado.append(Data_from_2007_2.objects.filter(**subquery[x]))
        elif indicator == 32:
            for x in range(0,len(subquery)):
                resultado.append(Data_from_2007_2.objects.filter(**subquery[x]))
        elif indicator == 33:
            for x in range(0,len(subquery)):
                resultado.append(Data_from_2007_2.objects.filter(**subquery[x]))
        elif indicator == 34:
            for x in range(0,len(subquery)):
                resultado.append(Data_from_2007_2.objects.filter(**subquery[x]))
        elif indicator == 35:
            for x in range(0,len(subquery)):
                resultado.append(Data_from_2007_2.objects.filter(**subquery[x]))
        elif indicator == 36:
            for x in range(0,len(subquery)):
                resultado.append(Data_from_2007_2.objects.filter(**subquery[x]))
        elif indicator == 37:
            for x in range(0,len(subquery)):
                resultado.append(Data_from_2007_2.objects.filter(**subquery[x]))
        elif indicator == 38:
            for x in range(0,len(subquery)):
                resultado.append(Data_from_2007_2.objects.filter(**subquery[x]).exclude(descon_bajos_ingresos__isnull=True))
                #Exclude descon_bajos_ingresos IS NULL
        elif indicator == 39:
            for x in range(0,len(subquery)):
                resultado.append(Data_from_2007_2.objects.filter(**subquery[x]).exclude(descon_horarios__isnull=True))
                #Exclude descon_horarios IS NULL
        elif indicator == 40:
            for x in range(0,len(subquery)):
                resultado.append(Data_from_2007_2.objects.filter(**subquery[x]).exclude(descon_estabil__isnull=True))
                #Exclude descon_estabil IS NULL
        elif indicator == 41:
            for x in range(0,len(subquery)):
                resultado.append(Data_from_2007_2.objects.filter(**subquery[x]).exclude(descon_amb_laboral__isnull=True))
                #Exclude descon_amb_laboral IS NULL
        elif indicator == 42:
            for x in range(0,len(subquery)):
                resultado.append(Data_from_2007_2.objects.filter(**subquery[x]).exclude(descon_activ__isnull=True))
                #Exclude descon_activ IS NULL

    return resultado

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
