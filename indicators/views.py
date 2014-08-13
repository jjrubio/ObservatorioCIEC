# -*- coding: utf-8 -*-
from django.shortcuts import HttpResponse, render_to_response
from django.template.context import RequestContext
from models import *
from disintegrations.models import *
from ENEMDU.models import *
import json
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder
from django.views.decorators.cache import cache_page
from django.core.cache import cache
import numpy as np
import statsmodels.api as sm
from django.core.files import File

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

def list_desagregation(request):
    disintegrations = Disintegration.objects.all()
    data = serializers.serialize('json', disintegrations)

    return HttpResponse(data, content_type='application/json')

def test(request):
    test = request.GET['test']
    data = ['2003', '2004', '2005']
    dato = json.dumps(data)
    return HttpResponse(dato, content_type='application/json')

@cache_page(60)
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

    if method_int == 1 :
        data_ENEMDU = Data_from_2003_4
        data_byWhere = get_data_byWhere(data_ENEMDU, indicator_int, represent_int, yearStart_int, trimStart_int, yearEnd_int, trimEnd_int).order_by('fexp')
        column_1 = get_column_1(data_byWhere, method_int, indicator_int)
        columns_2_3 = get_column_2_3(data_byWhere, disintegrations)
        column_2 = columns_2_3[0]
        column_3 = columns_2_3[1]
        column_4 = get_column_4(data_byWhere)
    else:
        data_ENEMDU = Data_from_2007_2
        data_byWhere = get_data_byWhere(data_ENEMDU, indicator_int, represent_int, yearStart_int, trimStart_int, yearEnd_int, trimEnd_int).order_by('fexp')
        column_1 = get_column_1(data_byWhere, method_int, indicator_int)
        columns_2_3 = get_column_2_3(data_byWhere, disintegrations)
        column_2 = columns_2_3[0]
        column_3 = columns_2_3[1]
        column_4 = get_column_4(data_byWhere)

    data_result = modelo_ind(column_1,[],[],column_4)
    # print(data_result)
    data = [column_1.tolist(), column_2.tolist(), column_3.tolist(), column_4.tolist()]

    message = json.dumps(data_result.tolist(), cls=DjangoJSONEncoder)
    return HttpResponse(message, content_type='application/json')

# Recordar que las filas de todos los vectores y matrices de entrada
# deben de estar ordenados por "fexp"
def modelo_ind(y,X,Z,fexp):

    # Calcular el indicador de cluster para corregir la matriz VCV
    clusvar = np.array([0],'int')
    ngroup=1
    last=fexp[0]

    for el in fexp:
        if last!=el:
            ngroup += 1
        clusvar1 = np.append(clusvar,ngroup)
    print clusvar1
    # Armar la regresion por OLS segun el modelo
    n = y.shape
    print n
    if not X and not Z:
        T = np.array([])
    elif not Z:
        n,colX = X.shape
        T=np.array(X[:,1:colX-1]) # Quitar por colinealidad 1 indicador por cada matriz
    else:
        n,colX = X.shape
        n,colZ = Z.shape
        T=np.array(X[:,1:colX-1],Z[:,1:colZ-1]) # Quitar por colinealidad 1 indicador por cada matriz

    T1 = np.append(T,np.ones([n[0],1]))
    # colX=colX-1 # Ajustar el num. de indicadores en X
    # colZ=colZ-1 # Ajustar el num. de indicadores en X
    # F=np.diag(fexp**0.5)
    # model=sm.OLS(np.asmatrix(F)*np.asmatrix(y),np.asmatrix(F)*np.asmatrix(T),"drop")
    # res_ols=model.fit()

    # Esta linea tiene que ser cambiada por la obtencion
    # de la "cluster robust variance"
    # vcv=res_ols.sigma*res_ols.normalized_cov_params

    # Construir la salida en el formato acordado
    # nOut=(colX+1)*(colZ+1)
    # output=np.zeros([nOut,2])
    # iX,iZ=0,0
    # offX,offZ=0,0
    # for iOut in range(nOut):
    #     # Incluir el coeficiente que corresponde a la tasa de cada combinacion y su varianza
    #     # que es la suma de las varianzas más 2 veces todas las covarianzas cruzadas
    #     output[iOut,1]=res_ols.params[0]
    #     output[iOut,2]=vcv[0,0]

    #     if (iZ>0):
    #         offZ=colX+1+iZ
    #         output[iOut,1]=output[iOut,1]+res_ols.params[offZ]
    #         output[iOut,2]=output[iOut,2]+vcv[offZ,offZ]+(2*vcv[0,offZ])

    #     if (iX>0):
    #         offX=1+iX
    #         output[iOut,1]=output[iOut,1]+res_ols.params[offX]
    #         output[iOut,2]=output[iOut,2]+vcv[offX,offX]+(2*vcv[0,offX])

    #     if (iZ<colZ-1):
    #         iZ+=1
    #     else:
    #         output[iOut,2]=output[iOut,2]+(2*vcv[offX,offZ])
    #         iZ=0
    #         iX+=1

    return y

def get_column_1(data, method_int, indicator_int):
    if method_int == 1:
        column_1 = data.values_list(get_filter()[indicator_int][0], flat=True)
    else:
        column_1 = data.values_list(get_filter()[indicator_int][1], flat=True)
    return np.asarray(column_1)


def get_column_2_3(data, disintegrations):
    columns =[]
    disintegrations_size = len(disintegrations)
    if disintegrations_size == 0:
        column_2 = None
        column_3 = None
    elif disintegrations_size == 1:
        option_1 = get_column_name_option(int(disintegrations[0]))
        filter_column_2_by = data.values_list(option_1, flat=True)
        column_2 = []
        types_option_1 = Type.objects.filter(disintegration_id = int(disintegrations[0])).values_list('name', flat=True)
        for i in range(1,len(types_option_1)+1):
            column_2.append([''])
            column_2[i-1] = [1 if x == types_option_1[i-1] else 0 for x in filter_column_2_by]
        column_3 = None
    elif disintegrations_size == 2:
        option_1 = get_column_name_option(int(disintegrations[0]))
        option_2 = get_column_name_option(int(disintegrations[1]))
        filter_column_2_by = data.values_list(option_1, flat=True)
        filter_column_3_by = data.values_list(option_2, flat=True)
        column_2 = []
        types_option_1 = Type.objects.filter(disintegration_id = int(disintegrations[0])).values_list('name', flat=True)
        for i in range(1,len(types_option_1)+1):
            column_2.append([''])
            column_2[i-1] = [1 if x == types_option_1[i-1] else 0 for x in filter_column_2_by]
        column_3 = []
        types_option_2 = Type.objects.filter(disintegration_id = int(disintegrations[1])).values_list('name', flat=True)
        for i in range(1,len(types_option_2)+1):
            column_3.append([''])
            column_3[i-1] = [1 if x == types_option_2[i-1] else 0 for x in filter_column_3_by]
    columns.append(np.asarray(column_2))
    columns.append(np.asarray(column_3))
    return columns

def get_column_4(data):
    column_4 = data.values_list("fexp", flat=True)
    return np.asarray(column_4)


def get_data_byWhere(data_ENEMDU, indicator_int, represent_int, yearStart_int, trimStart_int, yearEnd_int, trimEnd_int):
    data = data_ENEMDU.objects.none()
    trim_1 = trimStart_int
    trim_2 = 5

    for i in range(yearStart_int, yearEnd_int+1):
        if i == yearEnd_int:
            trim_2 = trimEnd_int+1

        for j in range(trim_1, trim_2):
            data = data | data_ENEMDU.objects.filter(anio=i, trimestre=j,**get_area(represent_int)).filter(**get_filter()[indicator_int][2]).exclude(**get_filter()[indicator_int][3])
            if j == 4:
                trim_1 = 1
    return data

def get_area(represent_int):
    if represent_int == 1:
        area = {}
    elif represent_int == 2:
        area = {'area': 'Urbano'}
    else:
        area = {'area': 'Rural'}
    return area

def list_by_no_denied(request):
    id_desagre = request.GET['id_desagregacion']
    datos = request.GET.getlist('data_filters[]')

    #Validacion entre desagregaciones
    if id_desagre == '1' or id_desagre == '3':
        disintegrations = Disintegration.objects.all()
        ids_value_list = disintegrations.values_list('id',flat=True)
        result = indicador_desagregacion(datos,ids_value_list)
        data = serializers.serialize('json', result)
    elif id_desagre == '2':
        disintegrations = Disintegration.objects.exclude(
            id__in=[10, 4, 5, 6, 8])
        ids_value_list = disintegrations.values_list('id',flat=True)
        result = indicador_desagregacion(datos,ids_value_list)
        data = serializers.serialize('json', result)
    elif id_desagre == '4':
        disintegrations = Disintegration.objects.exclude(
            id__in=[10, 2, 5, 6, 8])
        ids_value_list = disintegrations.values_list('id',flat=True)
        result = indicador_desagregacion(datos,ids_value_list)
        data = serializers.serialize('json', result)
    elif id_desagre == '5':
        disintegrations = Disintegration.objects.exclude(
            id__in=[10, 2, 4, 6, 8, 9])
        ids_value_list = disintegrations.values_list('id',flat=True)
        result = indicador_desagregacion(datos,ids_value_list)
        data = serializers.serialize('json', result)
    elif id_desagre == '6':
        disintegrations = Disintegration.objects.exclude(
            id__in=[10, 2, 4, 5, 8, 9])
        ids_value_list = disintegrations.values_list('id',flat=True)
        result = indicador_desagregacion(datos,ids_value_list)
        data = serializers.serialize('json', result)
    elif id_desagre == '7':
        disintegrations = Disintegration.objects.exclude(id__in=[8])
        ids_value_list = disintegrations.values_list('id',flat=True)
        result = indicador_desagregacion(datos,ids_value_list)
        data = serializers.serialize('json', result)
    elif id_desagre == '8':
        disintegrations = Disintegration.objects.exclude(
            id__in=[10, 2, 4, 5, 6, 7, 9])
        ids_value_list = disintegrations.values_list('id',flat=True)
        result = indicador_desagregacion(datos,ids_value_list)
        data = serializers.serialize('json', result)
    elif id_desagre == '9':
        disintegrations = Disintegration.objects.exclude(id__in=[10, 5, 6, 8])
        ids_value_list = disintegrations.values_list('id',flat=True)
        result = indicador_desagregacion(datos,ids_value_list)
        data = serializers.serialize('json', result)
    elif id_desagre == '10':
        disintegrations = Disintegration.objects.exclude(
            id__in=[2, 4, 5, 6, 8, 9])
        ids_value_list = disintegrations.values_list('id',flat=True)
        result = indicador_desagregacion(datos,ids_value_list)
        data = serializers.serialize('json', result)
    elif id_desagre == '11':
        disintegrations = Disintegration.objects.exclude(id__in=[12, 13])
        ids_value_list = disintegrations.values_list('id',flat=True)
        result = indicador_desagregacion(datos,ids_value_list)
        data = serializers.serialize('json', result)
    elif id_desagre == '12':
        disintegrations = Disintegration.objects.exclude(id__in=[11, 13])
        ids_value_list = disintegrations.values_list('id',flat=True)
        result = indicador_desagregacion(datos,ids_value_list)
        data = serializers.serialize('json', result)
    elif id_desagre == '13':
        disintegrations = Disintegration.objects.exclude(id__in=[11, 12])
        ids_value_list = disintegrations.values_list('id',flat=True)
        result = indicador_desagregacion(datos,ids_value_list)
        data = serializers.serialize('json', result)
     
    return HttpResponse(data, content_type='application/json')

def get_column_name_option(id_desagregation):
    if id_desagregation == 1:
        result = 'region_natural'
    elif id_desagregation == 2:
        result = 'ciudad_ind'
    elif id_desagregation == 3:
        result = 'genero'
    elif id_desagregation == 4:
        result = 'etnia'
    elif id_desagregation == 5:
        result = 'edad_group'
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
    else :
        result = ''
    return result

def get_filter():
    data = {1 : ['pet', 'pet', {}, {}],
                  2 : ['pea', 'pea', {}, {}],
                  3 : ['pea', 'pea', {'pet' : '1'}, {}],
                  4 : ['pei', 'pei', {'pet' : '1'}, {}],
                  5 : ['ocupa', 'ocupa', {'pet' : '1'}, {}],
                  6 : ['ocupa', 'ocupa', {'pea' : '1'}, {}],
                  7 : ['oplenos', 'oplenos', {'pea' : '1'}, {}],
                  8 : ['', 'ocupa*sect_formal', {'pea' : '1'}, {}],
                  9 : ['ocupa*sect_informal', 'ocupa*sect_informal', {'pea' : '1'}, {}],
                  10 : ['ocupa*sect_srvdom', 'ocupa*sect_srvdom', {'pea' : '1'}, {}],
                  11 : ['suboc', 'suboc', {'pea' : '1'}, {}],
                  12 : ['suboc1', 'suboc1', {'pea' : '1'}, {}],
                  13 : ['', 'suboc2', {'pea' : '1'}, {}],
                  14 : ['sub_inv', '', {'pea' : '1'}, {}],
                  15 : ['sub_informal', '', {'pea' : '1'}, {}],
                  16 : ['suboc*sect_moderno', '', {'pea' : '1'}, {}],#probar multiplicacion de columnas
                  17 : ['sub_inv*sect_moderno', '', {'pea' : '1'}, {}],
                  18 : ['suboc1*sec_moderno', '', {'pea' : '1'}, {}],
                  19 : ['deso', 'deso', {'pea' : '1'}, {}],
                  20 : ['', 'deaboc1', {'pea' : '1'}, {}],
                  21 : ['', 'deaboc2', {'pea' : '1'}, {}],
                  22 : ['deso1', 'deso1', {'pea' : '1'}, {}],
                  23 : ['deso2', 'deso2', {'pea' : '1'}, {}],
                  24 : ['oplenos', 'oplenos', {'ocupa' : '1'}, {}],
                  25 : ['suboc', 'suboc', {'ocupa' : '1'}, {}],
                  26 : ['ingrl', 'ingrl', {'ocupa' : '1'}, {'ingrl' : None}],
                  27 : ['', 'satis_laboral', {'ocupa' : '1'}, {'satis_laboral' : None}],
                  28 : ['', 'descon_bajos_ingresos', {'ocupa' : '1'}, {'descon_bajos_ingresos' : None}],
                  29 : ['', 'descon_horarios', {'ocupa' : '1'}, {'descon_horarios' : None}],
                  30 : ['', 'descon_estabil', {'ocupa' : '1'}, {'descon_estabil' : None}],
                  31 : ['', 'descon_amb_laboral', {'ocupa' : '1'}, {'descon_amb_laboral' : None}],
                  32 : ['', 'descon_activ', {'ocupa' : '1'}, {'descon_activ' : None}],
                  33 : ['anosaprob', 'anosaprob', {}, {'anosaprob' : None}],
                  34 : ['experiencia', 'experiencia', {}, {'experiencia' : None}],
                  35 : ['migracion_extranjera', 'migracion_extranjera', {}, {}],
                  36 : ['migracion_rural_urbano', 'migracion_rural_urbano', {}, {}],
                  37 : ['tamano_hogar', 'tamano_hogar', {'rela_jef' : '1'}, {}],
                  38 : ['hogar_completo', 'hogar_completo', {'rela_jef' : '1'}, {}],
                  39 : ['hogar_noFamiliar', 'hogar_noFamiliar', {'rela_jef' : '1'}, {}],
                  40 : ['ingreso_hogar', 'ingreso_hogar', {'rela_jef' : '1'}, {}],
                  41 : ['part_quehaceres', 'part_quehaceres', {}, {}],
                  42 : ['horas_part_quehaceres', 'horas_part_quehaceres', {}, {}],
                }
    return data

def table(request):
    trim_1 = request.GET['trim_1']
    trim_2 = request.GET['trim_2']
    yearStart = request.GET['yearStart']
    yearEnd = request.GET['yearEnd']

    arreglo = ['2003:4','2004:1','2004:2','2004:3','2004:4']
    data = json.dumps(arreglo)
    return HttpResponse(data, content_type='application/json')

def grafico(request):
    datos = [7.0, 6.9, 9.5, 14.5, 18.2, 21.5, 25.2, 26.5, 23.3, 18.3, 13.9, 9.6]

    data = json.dumps(datos)
    return HttpResponse(data,content_type='application/json')

def indicador_filtro(request):
    id_indicador = request.GET['id_indicator']

    if id_indicador == '1' or id_indicador == '2' or id_indicador == '3' or id_indicador == '4' or id_indicador == '5' or id_indicador == '6' or id_indicador == '7' or id_indicador == '8' or id_indicador == '9' or id_indicador == '10' or id_indicador == '11' or id_indicador == '12' or id_indicador == '13' or id_indicador == '14' or id_indicador == '15' or id_indicador == '16' or id_indicador == '17' or id_indicador == '18' or id_indicador == '19' or id_indicador == '20' or id_indicador == '21' or id_indicador == '22' or id_indicador == '23' or id_indicador == '24' or id_indicador == '25' or id_indicador == '26' or id_indicador == '27' or id_indicador == '28' or id_indicador == '29':
        disintegrations = Disintegration.objects.exclude(id__in=[7, 8, 9, 10, 11, 12, 13, 14])
        data = serializers.serialize('json', disintegrations)
    elif id_indicador == '30' or id_indicador == '31':
        disintegrations = Disintegration.objects.exclude(id__in=[11, 12, 13, 14])
        data = serializers.serialize('json', disintegrations)
    elif id_indicador == '32':
        disintegrations = Disintegration.objects.exclude(id__in=[11, 13, 14])
        data = serializers.serialize('json', disintegrations)
    elif id_indicador == '33' or id_indicador == '34' or id_indicador == '35' or id_indicador == '36' or id_indicador == '37' or id_indicador == '38':
        disintegrations = Disintegration.objects.exclude(id__in=[10, 11, 13, 14])
        data = serializers.serialize('json', disintegrations)
    elif id_indicador == '39' or id_indicador == '40' or id_indicador == '41':
        disintegrations = Disintegration.objects.exclude(id__in=[6, 7, 8, 9, 10])
        data = serializers.serialize('json', disintegrations)
    elif id_indicador == '42':
        disintegrations = Disintegration.objects.exclude(id__in=[2, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14])
        data = serializers.serialize('json', disintegrations)
    elif id_indicador == '43':
        disintegrations = Disintegration.objects.exclude(id__in=[7, 8, 9, 10, 11, 12, 13, 14])
        data = serializers.serialize('json', disintegrations)
    elif id_indicador == '44' or id_indicador == '45' or id_indicador == '46' or id_indicador == '47' or id_indicador == '48' or id_indicador == '49':
        disintegrations = Disintegration.objects.exclude(id__in=[7, 8, 9, 10, 11, 13, 14])
        data = serializers.serialize('json', disintegrations)

    return HttpResponse(data, content_type='application/json')

def indicador_desagregacion(datos,ids):
    result = []
    
    for i in range(0,len(ids)):
        for j in range(0,len(datos)):
            if ids[i] == int(datos [j]):
                result.append(int(datos[j]))

    disin = Disintegration.objects.filter(id__in=result)

    return disin
