#!/usr/bin/env python
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
import numpy as np
import statsmodels.api as sm
import statsmodels.stats as sms
from scipy.stats import t
import math
from datetime import datetime
from django.core.cache import cache


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
    permiso = True
    #if request.session.get('last_visit'):
       # last_visit_time = request.session.get('last_visit')
       # visits = request.session.get('visits', '0')
       # count = request.session.get('visits')

       # if (datetime.now() - datetime.strptime(last_visit_time[:-7], "%Y-%m-%d %H:%M:%S")).days > 0:
           # request.session['visits'] = visits + 1
           # request.session['last_visit'] = str(datetime.now())
           # permiso = True
   # else:
       # request.session['last_visit'] = str(datetime.now())
       # request.session['visits'] = 1

    json = indicators_detail(cat_id, subcat_id, ind_id)
    subcategories = Subcategory.objects.all()
    categories = Category.objects.all()
    disintegrations = Disintegration.objects.all()
    method_option = get_method_option(json[2][0]['id'])
    all_years = get_years_list()
    template = "indicator_calc.html"
    return render_to_response(template, context_instance=RequestContext(request, locals()))


# @cache_page(30)
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

    if method_int == 1:
        data_ENEMDU = Data_from_2003_4
    else:
        data_ENEMDU = Data_from_2007_2

    if not len(disintegrations) == 0:
        if len(disintegrations) == 1:
            cache_value = '%s_%s_%s_%s_%s_%s_%s_%s'%(indicator_int, represent_int, method_int, yearStart_int, trimStart_int, yearEnd_int, trimEnd_int, disintegrations[0])
            if(int(disintegrations[0]) == 2):
                data_ENEMDU = get_data_by_represent(data_ENEMDU, represent_int)
            else:
                data_ENEMDU = data_ENEMDU.objects.all()
        else:
            cache_value = '%s_%s_%s_%s_%s_%s_%s_%s_%s'%(indicator_int, represent_int, method_int, yearStart_int, trimStart_int, yearEnd_int, trimEnd_int, disintegrations[0], disintegrations[1])
            if(int(disintegrations[0]) == 2 or int(disintegrations[1]) == 2):
                data_ENEMDU = get_data_by_represent(data_ENEMDU, represent_int)
            else:
                data_ENEMDU = data_ENEMDU.objects.all()
    else:
        cache_value = '%s_%s_%s_%s_%s_%s_%s'%(indicator_int, represent_int, method_int, yearStart_int, trimStart_int, yearEnd_int, trimEnd_int)
        data_ENEMDU = data_ENEMDU.objects.all()

    data_result = []
    trim_1 = trimStart_int
    trim_2 = 5

    for i in range(yearStart_int, yearEnd_int+1):
        if i == yearEnd_int:
            trim_2 = trimEnd_int+1
        for j in range(trim_1, trim_2):
            represent_database = str(Structure.objects.get(anio=i, trim=j))
            if ((represent_int == 1 and represent_database == 'Nacional') or (represent_int == 2 and represent_database == 'Nacional')
                or (represent_int == 2 and represent_database == 'Urbana') or (represent_int == 3 and represent_database == 'Nacional')):
                data_byWhere = data_ENEMDU.filter(anio=i, trimestre=j,**get_filter_area(represent_int)).filter(**get_filter()[indicator_int][2]).exclude(**get_filter()[indicator_int][3]).order_by('fexp')
                column_1 = get_column_1(data_byWhere, method_int, indicator_int)
                columns_2_3 = get_column_2_3(data_byWhere, disintegrations, represent_int)
                column_2 = columns_2_3[0]
                column_3 = columns_2_3[1]
                column_dimensions = columns_2_3[2]
                column_N = columns_2_3[6]
                column_4 = get_column_4(data_byWhere)

                models_by_period = cache.get(cache_value)
                if models_by_period is None:
                    models_by_period = modelo_ind(column_1,column_2,column_3,column_4)
                    cache.set(cache_value, models_by_period, None)

                models_by_period_none = np.where(np.isnan(models_by_period), 0, models_by_period)
                data_result_by_period = [i, j, column_N, models_by_period_none.tolist()]
                data_result.append(data_result_by_period)

            if j == 4:
                trim_1 = 1

    column_titles = columns_2_3[3]
    column_name_d1 = column_titles[0]
    column_name_d2 = column_titles[1]
    column_types_d1 = columns_2_3[4]
    column_types_d2 = columns_2_3[5]

    disintegration = (Indicator.objects.get(id=indicator_int).name).encode('utf-8')
    if(column_dimensions[0] == 0):
        title = disintegration+' '+column_titles[0] +' a nivel '+get_area_name(represent_int)
    elif(column_dimensions[1] == 0):
        title = disintegration+' por '+column_titles[0] +' a nivel '+get_area_name(represent_int)
    else:
        title = disintegration+' por '+column_titles[0]+' - '+column_titles[1]+' a nivel '+get_area_name(represent_int)

    if(yearStart_int == yearEnd_int):
        years_title = str(yearStart_int)
    else:
        years_title = str(yearStart_int)+' - '+str(yearEnd_int)

    unit = Indicator.objects.get(id = indicator_int).unit.encode('utf-8')

    data_result.append(title)
    data_result.append(years_title)
    data_result.append(unit)
    data_result.append(column_dimensions)
    data_result.append(column_name_d1)
    data_result.append(column_name_d2)
    data_result.append(column_types_d1)
    data_result.append(column_types_d2)
    message = json.dumps(data_result, cls=DjangoJSONEncoder)
    return HttpResponse(message, content_type='application/json')


# Recordar que las filas de todos los vectores y matrices de entrada
# deben de estar ordenados por "fexp"
def modelo_ind(y,X,Z,fexp,conf=0.95,clusrobust=True):

    # Calcular el indicador de cluster para corregir la matriz VCV
    clusvar = np.array([],'int')
    ngroup=1
    last=fexp[0]

    for el in fexp:
        if abs(last-el)>0.01:
            ngroup += 1
            last=el
        clusvar=np.append(clusvar,ngroup)

    # Armar la regresion por OLS segun el modelo
    if not (X.any() or Z.any()):
        n = y.shape[0]
        T=np.ones([n,1])
        colX,colZ = 0,0
        nOut=1
        df=n-1
    elif not Z.any():
        n,colX = X.shape
        colZ = 0
        T=np.concatenate((np.ones([n,1]),X[:,1:]),axis=1)  # Quitar por colinealidad 1 indicador por cada matriz
        nOut=colX
        df=n-(colX-1)-1
    else:
        n,colX = X.shape
        n,colZ = Z.shape
        T=np.concatenate((np.ones([n,1]),X[:,1:], Z[:,1:]),axis=1) # Quitar por colinealidad 1 indicador por cada matriz
        nOut=colX*colZ
        df=n-(colX-1)-(colZ-1)-1

    fT=T
    irow = 0
    for row in T:
        fT[irow,:] =fexp[irow]*T[irow,:]
        irow += 1
    fy = fexp * y
    del T

    model=sm.OLS(fy,fT,"drop")
    res_ols=model.fit()

    # Ver si se quiere corregir la varianza por clusters o no
    if clusrobust:
        vcv=sms.sandwich_covariance.cov_cluster(res_ols,clusvar)
    else:
        vcv=res_ols.cov_params()

    # Construir la salida en el formato acordado
    output=np.zeros((nOut,4))
    iX,iZ=0,0
    offX,offZ=0,0
    crit=t.interval(conf,df)
    for iOut in range(nOut):
        # Incluir el coeficiente que corresponde a la tasa de cada combinacion y su varianza
        # que es la suma de las varianzas más 2 veces todas las covarianzas cruzadas
        if (iZ==0 and iX==0):
            output[iOut,0]=res_ols.params[0]
            output[iOut,1]=vcv[0,0]
        elif (iZ>0 and iX==0):
            offZ=(colX-1)+iZ
            output[iOut,0]=res_ols.params[0]+res_ols.params[offZ]
            output[iOut,1]=vcv[0,0]+vcv[offZ,offZ]+(2*vcv[0,offZ])
        elif (iZ==0 and iX>0):
            offX=iX
            output[iOut,0]=res_ols.params[0]+res_ols.params[offX]
            output[iOut,1]=vcv[0,0]+vcv[offX,offX]+(2*vcv[0,offX])
        else:
            offZ=(colX-1)+iZ
            offX=iX
            output[iOut,0]=res_ols.params[0]+res_ols.params[offX]+res_ols.params[offZ]
            output[iOut,1]=vcv[0,0]+vcv[offX,offX]+vcv[offZ,offZ]+(2*vcv[0,offX])+(2*vcv[0,offZ])+(2*vcv[offX,offZ])

        if (iZ<colZ-1):
            iZ+=1
        else:
            iZ=0
            iX+=1

        # Devolver la desv. estandar y no la varianza
        output[iOut,1]=output[iOut,1]**0.5

        # Calcular los límites para el intervalo de confianza
        output[iOut,2]=output[iOut,0]+(crit[0]*output[iOut,1])
        output[iOut,3]=output[iOut,0]+(crit[1]*output[iOut,1])

    return output


def get_column_1(data, method_int, indicator_int):
    if method_int == 1:
        if(indicator_int == 8 or indicator_int == 9 or indicator_int == 10 or indicator_int == 16 or indicator_int == 17 or indicator_int == 18):
            column_1_a = data.values_list(get_filter()[indicator_int][0], flat=True)
            column_1_b = data.values_list(get_filter()[indicator_int][4], flat=True)
            column_1 = [(x * y) for x, y in zip(column_1_a, column_1_b)]
        else:
            column_1 = data.values_list(get_filter()[indicator_int][0], flat=True)
    else:
        if(indicator_int == 8 or indicator_int == 9 or indicator_int == 10 or indicator_int == 16 or indicator_int == 17 or indicator_int == 18):
            column_1_a = data.values_list(get_filter()[indicator_int][1], flat=True)
            column_1_b = data.values_list(get_filter()[indicator_int][4], flat=True)
            column_1 = [(x * y) for x, y in zip(column_1_a, column_1_b)]
        else:
            column_1 = data.values_list(get_filter()[indicator_int][1], flat=True)
    column_1_array = np.array(list(column_1), 'float')
    return column_1_array


def get_column_2_3(data, disintegrations, represent_int):
    disintegrations_size = len(disintegrations)
    if disintegrations_size == 0:
        column_2_array = np.array([])
        column_3_array = np.array([])
        column_dimensions = [0, 0]
        column_titles = ['Sin Desagregaciones', '']
        column_types_d1 = ['Sin Desagregaciones']
        column_types_d2 = ['']
        sumaFexp = int(math.ceil(sum(data.values_list('fexp', flat=True))))
        column_N = [sumaFexp]
    elif disintegrations_size == 1:
        option_1 = get_column_name_option(int(disintegrations[0]))
        filter_column_2_by = data.values_list(option_1, flat=True)
        types_option_1 = get_type_by_represent(disintegrations[0], represent_int)
        column_2_array = np.array([], 'float')
        column_2_array = np.zeros((len(filter_column_2_by),len(types_option_1)))
        column_2_aux = list(filter_column_2_by)

        for i in range(1, len(filter_column_2_by)+1):
            column_2_array[i-1] = [1 if x == column_2_aux[i-1] else 0 for x in types_option_1]

        column_3_array = np.array([])
        column_dimensions = [len(types_option_1), 0]
        title_1 = Disintegration.objects.get(id=disintegrations[0]).name.encode('utf-8')
        column_titles = [title_1, '']
        column_types_d1 = []
        for d1 in types_option_1:
            column_types_d1.append(d1)
        column_types_d2 = ['']

        column_N = []
        for option in types_option_1:
            sumaFexp = int(math.ceil(sum(data.filter(**{option_1:option}).values_list('fexp', flat=True))))
            column_N.append(sumaFexp)
    elif disintegrations_size == 2:
        option_1 = get_column_name_option(int(disintegrations[0]))
        option_2 = get_column_name_option(int(disintegrations[1]))

        filter_column_2_by = data.values_list(option_1, flat=True)
        filter_column_3_by = data.values_list(option_2, flat=True)

        types_option_1 = get_type_by_represent(disintegrations[0], represent_int)
        types_option_2 = get_type_by_represent(disintegrations[1], represent_int)

        column_2_array = np.array([], 'float')
        column_2_array = np.zeros((len(filter_column_2_by),len(types_option_1)))
        column_2_aux = list(filter_column_2_by)
        for i in range(1, len(filter_column_2_by)+1):
            column_2_array[i-1] = [1 if x == column_2_aux[i-1] else 0 for x in types_option_1]

        column_3_array = np.array([], 'float')
        column_3_array = np.zeros((len(filter_column_3_by),len(types_option_2)))
        column_3_aux = list(filter_column_3_by)

        for j in range(0, 20):
            print column_3_aux[j]
        for i in range(1, len(filter_column_3_by)+1):
            column_3_array[i-1] = [1 if x == column_3_aux[i-1] else 0 for x in types_option_2]

        column_dimensions = [len(types_option_1), len(types_option_2)]
        title_1 = Disintegration.objects.get(id=disintegrations[0]).name.encode('utf-8')
        title_2 = Disintegration.objects.get(id=disintegrations[1]).name.encode('utf-8')
        column_titles = [title_1, title_2]

        column_N = []
        for optionA in types_option_1:
            for optionB in types_option_2:
                sumaFexp = int(math.ceil(sum(data.filter(**{option_1:optionA}).filter(**{option_2:optionB}).values_list('fexp', flat=True))))
                column_N.append(sumaFexp)

        column_types_d1 = []
        column_types_d2 = []
        for d1 in types_option_1:
            column_types_d1.append(d1)
        for d2 in types_option_2:
            column_types_d2.append(d2)

    columns = [column_2_array, column_3_array, column_dimensions, column_titles, column_types_d1, column_types_d2, column_N]
    return columns


def get_column_4(data):
    column_4 = data.values_list("fexp", flat=True)
    column_4_array = np.array(list(column_4), 'float')
    return column_4_array


def get_area_name(represent_int):
    if represent_int == 1:
        area = 'Nacional'
    elif represent_int == 2:
        area = 'Urbana'
    else:
        area = 'Rural'
    return area


def get_filter_area(represent_int):
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
        ids_value_list = disintegrations.values_list('id', flat=True)
        result = indicador_desagregacion(datos, ids_value_list)
        data = serializers.serialize('json', result)
    elif id_desagre == '2':
        disintegrations = Disintegration.objects.exclude(
            id__in=[4, 5, 6, 8, 10, 14])
        ids_value_list = disintegrations.values_list('id', flat=True)
        result = indicador_desagregacion(datos, ids_value_list)
        data = serializers.serialize('json', result)
    elif id_desagre == '4':
        disintegrations = Disintegration.objects.exclude(
            id__in=[2, 5, 6, 8, 10, 14])
        ids_value_list = disintegrations.values_list('id', flat=True)
        result = indicador_desagregacion(datos, ids_value_list)
        data = serializers.serialize('json', result)
    elif id_desagre == '5':
        disintegrations = Disintegration.objects.exclude(
            id__in=[2, 4, 6, 8, 9, 10, 14])
        ids_value_list = disintegrations.values_list('id', flat=True)
        result = indicador_desagregacion(datos, ids_value_list)
        data = serializers.serialize('json', result)
    elif id_desagre == '6':
        disintegrations = Disintegration.objects.exclude(
            id__in=[2, 4, 5, 8, 9, 10, 14])
        ids_value_list = disintegrations.values_list('id', flat=True)
        result = indicador_desagregacion(datos, ids_value_list)
        data = serializers.serialize('json', result)
    elif id_desagre == '7':
        disintegrations = Disintegration.objects.exclude(
            id__in=[8, 11, 13, 14])
        ids_value_list = disintegrations.values_list('id', flat=True)
        result = indicador_desagregacion(datos, ids_value_list)
        data = serializers.serialize('json', result)
    elif id_desagre == '8':
        disintegrations = Disintegration.objects.exclude(
            id__in=[2, 4, 5, 6, 7, 9, 10, 11, 12, 14])
        ids_value_list = disintegrations.values_list('id', flat=True)
        result = indicador_desagregacion(datos, ids_value_list)
        data = serializers.serialize('json', result)
    elif id_desagre == '9':
        disintegrations = Disintegration.objects.exclude(
            id__in=[5, 6, 8, 10, 11, 13, 14])
        ids_value_list = disintegrations.values_list('id', flat=True)
        result = indicador_desagregacion(datos, ids_value_list)
        data = serializers.serialize('json', result)
    elif id_desagre == '10':
        disintegrations = Disintegration.objects.exclude(
            id__in=[2, 4, 5, 6, 8, 9, 11, 12, 14])
        ids_value_list = disintegrations.values_list('id', flat=True)
        result = indicador_desagregacion(datos, ids_value_list)
        data = serializers.serialize('json', result)
    elif id_desagre == '11':
        disintegrations = Disintegration.objects.exclude(
            id__in=[7, 8, 9, 10, 12, 13, 14])
        ids_value_list = disintegrations.values_list('id', flat=True)
        result = indicador_desagregacion(datos, ids_value_list)
        data = serializers.serialize('json', result)
    elif id_desagre == '12':
        disintegrations = Disintegration.objects.exclude(
            id__in=[8, 10, 11, 13, 14])
        ids_value_list = disintegrations.values_list('id', flat=True)
        result = indicador_desagregacion(datos, ids_value_list)
        data = serializers.serialize('json', result)
    elif id_desagre == '13':
        disintegrations = Disintegration.objects.exclude(
            id__in=[7, 9, 11, 12, 14])
        ids_value_list = disintegrations.values_list('id', flat=True)
        result = indicador_desagregacion(datos, ids_value_list)
        data = serializers.serialize('json', result)
    elif id_desagre == '14':
        disintegrations = Disintegration.objects.exclude(
            id__in=[2, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13])
        ids_value_list = disintegrations.values_list('id', flat=True)
        result = indicador_desagregacion(datos, ids_value_list)
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
    elif id_desagregation == 14:
        result = 'condInact'
    else:
        result = ''
    return result


def get_filter():

    data ={
        1: ['pet', 'pet', {}, {}],
        2: ['pea', 'pea', {}, {'pea' : None}],
        3: ['pea', 'pea', {'pet' : '1'}, {}],
        4: ['pei', 'pei', {'pet' : '1'}, {}],
        5: ['ocupa', 'ocupa', {'pet' : '1'}, {}],
        6: ['ocupa', 'ocupa', {'pea' : '1'}, {}],
        7: ['oplenos', 'oplenos', {'pea' : '1'}, {}],
        8: ['', 'ocupa', {'pea' : '1'}, {}, 'sect_formal'],
        9: ['ocupa', 'ocupa', {'pea' : '1'}, {}, 'sect_informal'],
        10: ['ocupa', 'ocupa', {'pea' : '1'}, {}, 'sect_srvdom'],
        11: ['suboc', 'suboc', {'pea' : '1'}, {}],
        12: ['suboc1', 'suboc1', {'pea' : '1'}, {}],
        13: ['', 'suboc2', {'pea' : '1'}, {}],
        14: ['sub_inv', '', {'pea' : '1'}, {}],
        15: ['sub_informal', '', {'pea' : '1'}, {}],
        16: ['suboc', '', {'pea' : '1'}, {}, 'sect_moderno'],
        17: ['sub_inv', '', {'pea' : '1'}, {}, 'sect_moderno'],
        18: ['suboc1', '', {'pea' : '1'}, {}, 'sect_moderno'],
        19: ['deso', 'deso', {'pea' : '1'}, {}],
        20: ['', 'deaboc1', {'pea' : '1'}, {}],
        21: ['', 'deaboc2', {'pea' : '1'}, {}],
        22: ['deso1', 'deso1', {'pea' : '1'}, {}],
        23: ['deso2', 'deso2', {'pea' : '1'}, {}],
        24: ['rentista', 'rentista', {'pei' : '1'}, {'rentista' : None}],
        25: ['jubil', 'jubil', {'pei' : '1'}, {'jubil' : None}],
        26: ['estudiant', 'estudiant', {'pei' : '1'}, {'estudiant' : None}],
        27: ['amaCasa', 'amaCasa', {'pei' : '1'}, {'amaCasa' : None}],
        28: ['incapacit', 'incapacit', {'pei' : '1'}, {'incapacit' : None}],
        29: ['otro', 'otro', {'pei' : '1'}, {'otro' : None}],
        30: ['oplenos', 'oplenos', {'ocupa' : '1'}, {}],
        31: ['suboc', 'suboc', {'ocupa' : '1'}, {}],
        32: ['ingrl', 'ingrl', {'ocupa' : '1'}, {'ingrl' : None}],
        33: ['', 'satis_laboral', {'ocupa' : '1'}, {'satis_laboral' : None}],
        34: ['', 'descon_bajos_ingresos', {'ocupa' : '1'}, {'descon_bajos_ingresos' : None}],
        35: ['', 'descon_horarios', {'ocupa' : '1'}, {'descon_horarios' : None}],
        36: ['', 'descon_estabil', {'ocupa' : '1'}, {'descon_estabil' : None}],
        37: ['', 'descon_amb_laboral', {'ocupa' : '1'}, {'descon_amb_laboral' : None}],
        38: ['', 'descon_activ', {'ocupa' : '1'}, {'descon_activ' : None}],
        39: ['anosaprob', 'anosaprob', {}, {'anosaprob' : None}],
        40: ['analfabeta', 'analfabeta', {}, {'analfabeta' : None}],
        41: ['experiencia', 'experiencia', {}, {'experiencia' : None}],
        42: ['migracion_extranjera', 'migracion_extranjera', {}, {'migracion_extranjera' : None}],
        43: ['migracion_rural_urbano', 'migracion_rural_urbano', {}, {'migracion_rural_urbano' : None}],
        44: ['tamano_hogar', 'tamano_hogar', {'rela_jef' : '1'}, {}],
        45: ['hogar_completo', 'hogar_completo', {'rela_jef' : '1'}, {}],
        46: ['hogar_noFamiliar', 'hogar_noFamiliar', {'rela_jef' : '1'}, {}],
        47: ['ingreso_hogar', 'ingreso_hogar', {'rela_jef' : '1'}, {}],
        48: ['part_quehaceres', 'part_quehaceres', {}, {'part_quehaceres' : None}],
        49: ['horas_part_quehaceres', 'horas_part_quehaceres', {}, {'horas_part_quehaceres' : None}],
    }
    return data


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

    for i in range(0, len(ids)):
        for j in range(0, len(datos)):
            if ids[i] == int(datos[j]):
                result.append(int(datos[j]))

    disin = Disintegration.objects.filter(id__in=result)

    return disin


def list_desagregation(request):
    disintegrations = Disintegration.objects.all()
    data = serializers.serialize('json', disintegrations)

    return HttpResponse(data, content_type='application/json')


def get_data_by_represent(data_ENEMDU, represent_int):
    if(represent_int == 2):
        data = data_ENEMDU.objects.exclude(ciudad_ind='Resto Pais Rural')
    elif(represent_int == 3):
        data = data_ENEMDU.objects.exclude(ciudad_ind='Resto Pais Urbano')
    else:
        data = data_ENEMDU.objects.all()
    return data


def get_type_by_represent(disintegrations_pos, represent_int):
    if(int(disintegrations_pos) == 2):
        if(represent_int == 2):
            types_option = Type.objects.filter(disintegration_id = int(disintegrations_pos)).exclude(name='Resto Pais Rural').values_list('name', flat=True)
        elif(represent_int == 3):
            types_option = Type.objects.filter(disintegration_id = int(disintegrations_pos)).exclude(name='Resto Pais Urbano').values_list('name', flat=True)
        else:
            types_option = Type.objects.filter(disintegration_id = int(disintegrations_pos)).values_list('name', flat=True)
    else:
        types_option = Type.objects.filter(disintegration_id = int(disintegrations_pos)).values_list('name', flat=True)
    return types_option


def get_last_full_year(request):
    year = Data_from_2007_2.objects.values_list('anio', 'trimestre').distinct().last()
    last_full_year = [year[0], year[1]]
    data = json.dumps(last_full_year)
    return HttpResponse(data, content_type='application/json')


def get_method_option(indicator):
    method_1_valor = get_filter()[indicator][0]
    method_2_valor = get_filter()[indicator][1]

    if method_1_valor == '':
        method_option = 2
    elif method_2_valor == '':
        method_option = 1
    else:
        method_option = 3
    return method_option


def get_years_list():
    method_1_years = Data_from_2003_4.objects.values_list('anio').distinct()
    method_2_years = Data_from_2007_2.objects.values_list('anio').distinct()
    method_2_last_year = Data_from_2007_2.objects.values_list('anio').distinct().last()
    method_2_last_trims = Data_from_2007_2.objects.filter(anio = method_2_last_year[0]).values_list('trimestre').distinct()
    all_years = [method_1_years, method_2_years, method_2_last_trims]
    return all_years
