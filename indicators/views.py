#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.shortcuts import HttpResponse, HttpResponseRedirect, render_to_response
from django.template.context import RequestContext
from models import *
from disintegrations.models import *
from ENEMDU.models import *
import json
from django.core import serializers
from json import JSONEncoder
import pickle
import numpy as np
import statsmodels.api as sm
import statsmodels.stats as sms
from scipy.stats import t
import math
from django.core.cache import cache
import time
from datetime import datetime
from django.contrib.sessions.models import Session
from django.db.models import Sum
# from task import trada


class PythonObjectEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (list, dict, str, unicode, int, float, bool, type(None))):
            return JSONEncoder.default(self, obj)
        return {'_python_object': pickle.dumps(obj)}

def as_python_object(dct):
    if '_python_object' in dct:
        return pickle.loads(str(dct['_python_object']))
    return dct


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
    # if request.session.get('last_visit'):
    #    last_visit_time = request.session.get('last_visit')
    #    visits = request.session.get('visits', '0')
    #    count = request.session.get('visits')

    #    if (datetime.now() - datetime.strptime(last_visit_time[:-7], "%Y-%m-%d %H:%M:%S")).days > 0:
    #        request.session['visits'] = visits + 1
    #        request.session['last_visit'] = str(datetime.now())
    #        permiso = True
    # else:
    #    request.session['last_visit'] = str(datetime.now())
    #    request.session['visits'] = 1

    json = indicators_detail(cat_id, subcat_id, ind_id)
    subcategories = Subcategory.objects.all()
    categories = Category.objects.all()
    disintegrations = Disintegration.objects.all()
    method_option = get_method_option(json[2][0]['id'])
    all_years = get_years_list()
    template = "indicator_calc.html"
    return render_to_response(template, context_instance=RequestContext(request, locals()))


def calc_result(request):
    indicator = request.GET['indicator']
    represent = request.GET['represent']
    method = request.GET['method']
    yearStart = request.GET['yearStart']
    trimStart = request.GET['trimStart']
    yearEnd = request.GET['yearEnd']
    trimEnd = request.GET['trimEnd']
    confidence_level = request.GET['confidence_level']
    disintegrations = request.GET.getlist('disintegrations[]')

    indicator_int = int(indicator)
    represent_int = int(represent)
    method_int = int(method)
    yearStart_int = int(yearStart)
    trimStart_int = int(trimStart)
    yearEnd_int = int(yearEnd)
    trimEnd_int = int(trimEnd)
    confidence_level_int = float(confidence_level)/100

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

    data_result = cache.get(cache_value)
    if data_result is None:

        data_result = []
        ban = 0
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

                    models_by_period = modelo_final(column_1,column_2,column_3,column_4, confidence_level_int)
                    models_by_period_none = np.where(np.isnan(models_by_period), 0, models_by_period)
                    data_result_by_period = [i, j, column_N, models_by_period_none.tolist()]
                    data_result.append(data_result_by_period)

                    if (ban == 0):
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

                        ban = 1

                if j == 4:
                    trim_1 = 1

        if ban == 1:
            data_result.append(title)
            data_result.append(years_title)
            data_result.append(unit)
            data_result.append(column_dimensions)
            data_result.append(column_name_d1)
            data_result.append(column_name_d2)
            data_result.append(column_types_d1)
            data_result.append(column_types_d2)
            indicator_counter = Indicator.objects.get(id=indicator_int).counter + 1
            update_indicator_counter = Indicator.objects.filter(id=indicator_int).update(counter=indicator_counter)
            cache.set(cache_value, data_result, None)

    message = json.dumps(data_result, cls=PythonObjectEncoder)
    return HttpResponse(message, content_type='application/json')


def modelo_ind(y,X,Z,fexp,conf=0.95,colin_thres=30):

    # Armar la regresion por OLS segun el modelo
    if not (X.any() or Z.any()):
        n = y.shape[0]
        T=np.ones([n,1])
        colX,colZ = 0,0
        nOut=1
        df=n-1
    elif not Z.any():
        # Descartar categorias base con menos del minimo de observaciones
        X=remove_colinear_base(X, colin_thres)
        n,colX = X.shape
        colZ = 0
        T=np.concatenate((np.ones([n,1]),X[:,1:]),axis=1)  # Quitar por colinealidad 1 indicador por cada matriz
        nOut=colX
        df=n-(colX-1)-1
    else:
        # Descartar categorias base con menos del minimo de observaciones
        X=remove_colinear_base(X, colin_thres)
        Z=remove_colinear_base(Z, colin_thres)
        n,colX = X.shape
        n,colZ = Z.shape
        T=np.concatenate((np.ones([n,1]),X[:,1:], Z[:,1:]),axis=1) # Quitar por colinealidad 1 indicador por cada matriz
        # Crear las interacciones entre las variables categoricas
        for iX in range(colX-1):
            for iZ in range(colZ-1):
                T=np.concatenate((T,(X[:,iX+1]*Z[:,iZ+1]).reshape(n,1)),axis=1)
        nOut=colX*colZ
        df=n-(colX-1)-(colZ-1)-(colX-1)*(colZ-1)-1

    # Este procedimiento es equivalente a la "pweights regression" en Stata 13
    # validando que no existan cruces (grupos) con cruces con "pocos" elementos
    nParams=T.shape[1]
    nancol_T = ( np.sum(T,axis=0) <= colin_thres )
    fy, fT , irow = float('nan')*y, float('nan')*T, 0
    for row in T:
        if np.sum(row[nancol_T])>0:
            # No agregar filas que caigan en categorias con "pocos" elementos
            pass
        else:
            fy[irow]=(fexp[irow]**0.5) * y[irow]
            fT[irow,:]=(fexp[irow]**0.5) * T[irow,:]
        irow += 1
    fT = fT[:,~nancol_T] # Eliminar columnas con "pocos" elementos
    del y,T

    model=sm.OLS(fy,fT,"drop",True)
    res_ols=model.fit()
    hac_vcv=sms.sandwich_covariance.cov_hac(res_ols,0)
    params=float('nan')*np.ones(nParams)
    params[~nancol_T]=res_ols.params
    vcv=float('nan')*np.ones((nParams,nParams))
    irow,cidx=0,0
    while irow<nParams:
        if not nancol_T[irow]:
            vcv[irow,~nancol_T]=hac_vcv[cidx,:]
            cidx+=1
        irow+=1

    # Construir la salida en el formato acordado
    output=float('nan')*np.ones((nOut,4))
    iX,iZ=0,0
    crit=t.interval(conf,df)
    for iOut in range(nOut):
        # Incluir el coeficiente que corresponde a la tasa de cada combinacion y su varianza
        # que es la suma de las varianzas más 2 veces todas las covarianzas cruzadas
        if (iZ==0 and iX==0):
            output[iOut,0]=params[0]
            output[iOut,1]=vcv[0,0]
        elif (iZ>0 and iX==0):
            offZ=(colX-1)+iZ
            output[iOut,0]=params[0]+params[offZ]
            output[iOut,1]=vcv[0,0]+vcv[offZ,offZ]+(2*vcv[0,offZ])
        elif (iZ==0 and iX>0):
            offX=iX
            output[iOut,0]=params[0]+params[offX]
            output[iOut,1]=vcv[0,0]+vcv[offX,offX]+(2*vcv[0,offX])
        else:
            offZ=(colX-1)+iZ
            offX=iX
            offXZ=(colX-1)+(colZ-1)+(colZ-1)*(iX-1)+iZ
            output[iOut,0]=params[0]+params[offX]+params[offZ]+params[offXZ]
            output[iOut,1]=vcv[0,0]+vcv[offX,offX]+vcv[offZ,offZ]+vcv[offXZ,offXZ]+(2*vcv[0,offX])+(2*vcv[0,offZ])+(2*vcv[0,offXZ])+(2*vcv[offX,offZ])+(2*vcv[offX,offXZ])+(2*vcv[offZ,offXZ])

        # Devolver la desv. estandar y no la varianza
        output[iOut,1]=output[iOut,1]**0.5

        # Calcular los límites para el intervalo de confianza
        output[iOut,2]=output[iOut,0]+(crit[0]*output[iOut,1])
        output[iOut,3]=output[iOut,0]+(crit[1]*output[iOut,1])

        if (iZ<colZ-1):
            iZ+=1
        else:
            iZ=0
            iX+=1

    return output

def remove_colinear_base(mat, colin_thres):
    X, icol = np.copy(mat), 0
    while True:
        if sum(X[:,icol])>colin_thres:
            break
        X=np.delete(X,icol,axis=1)
        icol+=1
    return X


def modelo_final(y, X, Z, fexp, conf = 0.95, colin_thres = 30):
    if not (X.any() or Z.any()):
        P = modelo_ind(y, X, Z, fexp, conf, colin_thres)
    elif not Z.any():
        nx = int(np.size(X, 1))
        flag_x = 0
        x_tot = np.sum(X, 0)

        x_temp = np.copy(X[:,0])
        x_dict = np.empty((nx, 2), dtype=int)
        x_dict[:,0] = range(nx)
        x_dict[:,1] = range(nx)

        if x_tot[0] < 30:
            flag_x += 1
            for i in range(1, nx, 1):
                if x_tot[i] >= 30:
                    X[:,0] = X[:,i]
                    x_dict[0,1] = i
                    x_dict[i,1] = 0
                    X[:,i] = x_temp

                break

        #Calcular los predicts con input ordenado
        P = modelo_ind(y, X, Z, fexp, conf, colin_thres)

        #reordenar los predict
        #reordenar si se cambio la primera columna de X y no de Z
        if (flag_x==1):
            sx = x_dict[0,1]
            P_temp = np.copy(P[0, :])
            P[0,:] = P[sx, :]
            P[sx,:] = P_temp

    else:
        nx = int(np.size(X, 1))
        nz = int(np.size(Z, 1))
        flag_x = 0
        flag_z = 0
        x_tot = np.sum(X, 0)
        z_tot = np.sum(Z, 0)

        x_temp = np.copy(X[:,0])
        x_dict = np.empty((nx, 2), dtype=int)
        x_dict[:,0] = range(nx)
        x_dict[:,1] = range(nx)

        z_temp = np.copy(Z[:,0])
        z_dict = np.empty((nz, 2), dtype=int)
        z_dict[:,0] = range(nz)
        z_dict[:,1] = range(nz)

        if x_tot[0] < 30:
            flag_x += 1
            for i in range(1, nx, 1):
                if x_tot[i] >= 30:
                    X[:,0] = X[:,i]
                    x_dict[0,1] = i
                    x_dict[i,1] = 0
                    X[:,i] = x_temp

                break

        if z_tot[0] < 30:
            flag_z += 1
            for i in range(1, nz, 1):
                if z_tot[i] >= 30:
                    Z[:,0] = Z[:,i]
                    z_dict[0,1] = i
                    z_dict[i,1] = 0
                    Z[:,i] = z_temp

                break
        #Calcular los predicts con input ordenado
        P = modelo_ind(y, X, Z, fexp, conf, colin_thres)
        #reordenar los predict
        #reordenar si se cambio la primera columna de X y no de Z
        if (flag_x==1 and flag_z==0):
            sx = x_dict[0,1]
            P_temp = np.copy(P[:nz,:])
            s_range = range(sx*nz, sx*nz+nz)
            P[:nz,:] = P[s_range, :]
            P[s_range, :] = P_temp
        #reordenar si se cambio la primera columna de Z y no de X
        elif (flag_x==0 and flag_z==1):
            sz = z_dict[0,1]
            s_range_a = range(0, nz*nx, nz)
            P_temp = np.copy(P[s_range_a])
            s_range_b = range(sz, nz*nx, nz)
            P[s_range_a] = P[s_range_b]
            P[s_range_b] = P_temp
        #reordenar si se cambiaron las primeras columnas de X y Z
        elif (flag_x==1 and flag_z==1):
            #reordenar el bloque base correspondiente a X
            sx = x_dict[0,1]
            P_temp = np.copy(P[:nz,:])
            s_range = range(sx*nz, sx*nz+nz)
            P[:nz,:] = P[s_range, :]
            P[s_range, :] = P_temp
            #reordenar las bases de Z en los diferentes bloques de X ya ordenados
            sz = z_dict[0,1]
            s_range_a = range(0, nz*nx, nz)
            P_temp = np.copy(P[s_range_a])
            s_range_b = range(sz, nz*nx, nz)
            P[s_range_a] = P[s_range_b]
            P[s_range_b] = P_temp

    return P


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

        for i in range(0, len(filter_column_2_by)):
            if column_2_aux[i] == None:
                pass
            else:
                column_2_array[i] = [1 if x == column_2_aux[i] else 0 for x in types_option_1]

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
            sumaFexp = int(math.ceil(sum(data.filter(**{option_1:option}).exclude(**{option_1:None}).values_list('fexp', flat=True))))
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
        for i in range(0, len(filter_column_2_by)):
            if column_2_aux[i] == None:
                pass
            else:
                column_2_array[i] = [1 if x == column_2_aux[i] else 0 for x in types_option_1]

        column_3_array = np.array([], 'float')
        column_3_array = np.zeros((len(filter_column_3_by),len(types_option_2)))
        column_3_aux = list(filter_column_3_by)
        for i in range(0, len(filter_column_3_by)):
            if column_2_aux[i] == None:
                pass
            else:
                column_3_array[i] = [1 if x == column_3_aux[i] else 0 for x in types_option_2]

        column_dimensions = [len(types_option_1), len(types_option_2)]
        title_1 = Disintegration.objects.get(id=disintegrations[0]).name.encode('utf-8')
        title_2 = Disintegration.objects.get(id=disintegrations[1]).name.encode('utf-8')
        column_titles = [title_1, title_2]

        # column_N = np.array([], 'float')
        # column_N = np.zeros((len(types_option_1),len(types_option_2)))
        # for optionA in types_option_1:
        #     column_N = [int(math.ceil(sum(data.filter(**{option_1:optionA}).filter(**{option_2:optionB}).values_list('fexp', flat=True)))) for optionB in types_option_2]
        column_N = []
        for optionA in types_option_1:
            for optionB in types_option_2:
                sumaFexp = int(math.ceil(sum(data.filter(**{option_1:optionA}).filter(**{option_2:optionB}).exclude(**{option_1:None}).exclude(**{option_2:None}).values_list('fexp', flat=True))))
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
    if id_desagre == '1':
        disintegrations = Disintegration.objects.exclude(id__in=[2, 4])
        ids_value_list = disintegrations.values_list('id', flat=True)
        result = indicador_desagregacion(datos, ids_value_list)
        data = serializers.serialize('json', result)
    elif id_desagre == '2':
        disintegrations = Disintegration.objects.exclude(
            id__in=[1, 4, 5, 6, 8, 10, 14])
        ids_value_list = disintegrations.values_list('id', flat=True)
        result = indicador_desagregacion(datos, ids_value_list)
        data = serializers.serialize('json', result)
    elif id_desagre == '3':
        disintegrations = Disintegration.objects.all()
        ids_value_list = disintegrations.values_list('id', flat=True)
        result = indicador_desagregacion(datos, ids_value_list)
        data = serializers.serialize('json', result)
    elif id_desagre == '4':
        disintegrations = Disintegration.objects.exclude(
            id__in=[1, 2, 5, 6, 8, 10, 14])
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
            id__in=[2, 4, 5, 6, 7, 9, 10, 11, 12, 13, 14])
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
            id__in=[2, 4, 5, 6, 8, 9, 11, 12, 13, 14])
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
            id__in=[7, 8, 9, 10, 11, 12, 14])
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

    if id_indicador == '1':
        disintegrations = Disintegration.objects.exclude(id__in=[4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14])
        data = serializers.serialize('json', disintegrations)
    elif id_indicador == '2' or id_indicador == '3' or id_indicador == '4' or id_indicador == '5' or id_indicador == '6' or id_indicador == '7' or id_indicador == '8' or id_indicador == '9' or id_indicador == '10' or id_indicador == '11' or id_indicador == '12' or id_indicador == '13' or id_indicador == '14' or id_indicador == '15' or id_indicador == '16' or id_indicador == '17' or id_indicador == '18' or id_indicador == '19' or id_indicador == '20' or id_indicador == '21' or id_indicador == '22' or id_indicador == '23' or id_indicador == '24' or id_indicador == '25' or id_indicador == '26' or id_indicador == '43':
        disintegrations = Disintegration.objects.exclude(id__in=[7, 8, 9, 10, 11, 12, 13, 14])
        data = serializers.serialize('json', disintegrations)
    elif id_indicador == '27':
        disintegrations = Disintegration.objects.exclude(id__in=[7, 8, 9, 11, 12, 13, 14])
        data = serializers.serialize('json', disintegrations)
    elif id_indicador == '28' or id_indicador == '29' or id_indicador == '30' or id_indicador == '31':
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


def indicator_filter_list(id):
    if id == 1:
        disintegrations = [1, 2, 3]
    elif id == 2 or id == 3 or id == 4 or id == 5 or id == 6 or id == 7 or id == 8 or id == 9 or id == 10 or id == 11 or id == 12 or id == 13 or id == 14 or id == 15 or id == 16 or id == 17 or id == 18 or id == 19 or id == 20 or id == 21 or id == 22 or id == 23 or id == 24 or id == 25 or id == 26 or id == 43:
        disintegrations = [1, 2, 3, 4, 5, 6]
    elif id == 27:
        disintegrations = [1, 2, 3, 4, 5, 6, 10]
    elif id == 28 or id == 29 or id == 30 or id == 31:
        disintegrations = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    elif id == 32:
        disintegrations = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12]
    elif id == 33 or id == 34 or id == 35 or id == 36 or id == 37 or id == 38:
        disintegrations = [1, 2, 3, 4, 5, 6, 7, 8, 9, 12]
    elif id == 39 or id == 40 or id == 41:
        disintegrations = [1, 2, 3, 4, 5, 11, 12, 13, 14]
    elif id == 42:
        disintegrations = [1, 3]
    elif id == 44 or id == 45 or id == 46 or id == 47 or id == 48 or id == 49:
        disintegrations = [1, 2, 3, 4, 5, 6, 12]
    return disintegrations


def disintegration_denied_list(dis):
    if dis == 1:
        denied = [2, 4]
    elif dis == 2:
        denied = [1, 4, 5, 6, 8, 10, 14]
    elif dis == 3:
        denied = []
    elif dis == 4:
        denied = [1, 2, 5, 6, 8, 10, 14]
    elif dis == 5:
        denied = [2, 4, 6, 8, 9, 10, 14]
    elif dis == 6:
        denied = [2, 4, 5, 8, 9, 10, 14]
    elif dis == 7:
        denied = [8, 11, 13, 14]
    elif dis == 8:
        denied = [2, 4, 5, 6, 7, 9, 10, 11, 12, 13, 14]
    elif dis == 9:
        denied = [5, 6, 8, 10, 11, 13, 14]
    elif dis == 10:
        denied = [2, 4, 5, 6, 8, 9, 11, 12, 13, 14]
    elif dis == 11:
        denied = [7, 8, 9, 10, 12, 13, 14]
    elif dis == 12:
        denied = [8, 10, 11, 13, 14]
    elif dis == 13:
        denied = [7, 8, 9, 10, 11, 12, 14]
    elif dis == 14:
        denied = [2, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
    return denied


def numero_consultas(request):
    represent = request.GET['represent']
    yearStart = request.GET['yearStart']
    trimStart = request.GET['trimStart']
    yearEnd = request.GET['yearEnd']
    trimEnd = request.GET['trimEnd']
    represent_int = int(represent)
    yearStart_int = int(yearStart)
    trimStart_int = int(trimStart)
    yearEnd_int = int(yearEnd)
    trimEnd_int = int(trimEnd)

    trim_1 = trimStart_int
    trim_2 = 5
    num = 0

    for i in range(yearStart_int, yearEnd_int+1):
        if i == yearEnd_int:
            trim_2 = trimEnd_int+1
        for j in range(trim_1, trim_2):
            represent_database = str(Structure.objects.get(anio=i, trim=j))
            if ((represent_int == 1 and represent_database == 'Nacional') or (represent_int == 2 and represent_database == 'Nacional')
                or (represent_int == 2 and represent_database == 'Urbana') or (represent_int == 3 and represent_database == 'Nacional')):
                num += 1
    message = json.dumps(num)
    return HttpResponse(message, content_type='application/json')


def calc_data(ind, data_ENEMDU, yearStart_int, yearEnd_int, trimStart_int, trimEnd_int, yearStart_aux, yearEnd_aux, trimStart_aux, trimEnd_aux, represent, method, disintegrations, cache_value):
    data_result = []
    ban = 0
    trim_1 = trimStart_aux
    trim_2 = 5

    for i in range(yearStart_aux, yearEnd_aux+1):
        if i == yearEnd_int:
            trim_2 = trimEnd_aux + 1
        for j in range(trim_1, trim_2):
            represent_database = str(Structure.objects.get(anio=i, trim=j))
            if ((represent == 1 and represent_database == 'Nacional') or (represent == 2 and represent_database == 'Nacional')
                or (represent == 2 and represent_database == 'Urbana') or (represent == 3 and represent_database == 'Nacional')):
                # print i,j
                data_byWhere = data_ENEMDU.filter(anio=i, trimestre=j,**get_filter_area(represent)).filter(**get_filter()[ind][2]).exclude(**get_filter()[ind][3]).order_by('fexp')
                column_1 = get_column_1(data_byWhere, method, ind)
                columns_2_3 = get_column_2_3(data_byWhere, disintegrations, represent)
                column_2 = columns_2_3[0]
                column_3 = columns_2_3[1]
                column_dimensions = columns_2_3[2]
                column_N = columns_2_3[6]
                column_4 = get_column_4(data_byWhere)

                models_by_period = modelo_final(column_1,column_2,column_3,column_4)
                models_by_period_none = np.where(np.isnan(models_by_period), 0, models_by_period)
                data_result_by_period = [i, j, column_N, models_by_period_none.tolist()]
                data_result.append(data_result_by_period)

                if (ban == 0):
                    column_titles = columns_2_3[3]
                    column_name_d1 = column_titles[0]
                    column_name_d2 = column_titles[1]
                    column_types_d1 = columns_2_3[4]
                    column_types_d2 = columns_2_3[5]

                    disintegration = (Indicator.objects.get(id=ind).name).encode('utf-8')
                    if(column_dimensions[0] == 0):
                        title = disintegration+' '+column_titles[0] +' a nivel '+get_area_name(represent)
                    elif(column_dimensions[1] == 0):
                        title = disintegration+' por '+column_titles[0] +' a nivel '+get_area_name(represent)
                    else:
                        title = disintegration+' por '+column_titles[0]+' - '+column_titles[1]+' a nivel '+get_area_name(represent)

                    if(yearStart_aux == yearEnd_aux):
                        years_title = str(yearStart_aux)
                    else:
                        years_title = str(yearStart_aux)+' - '+str(yearEnd_aux)

                    unit = Indicator.objects.get(id = ind).unit.encode('utf-8')

                    ban = 1

            if j == 4:
                trim_1 = 1

    if ban == 1:
        data_result.append(title)
        data_result.append(years_title)
        data_result.append(unit)
        data_result.append(column_dimensions)
        data_result.append(column_name_d1)
        data_result.append(column_name_d2)
        data_result.append(column_types_d1)
        data_result.append(column_types_d2)
        cache.set(cache_value, data_result, None)
    return 1


def generar_cache(request):
    user = request.user
    is_super_user = user.is_superuser

    if is_super_user:
        data_result = []
        indicators = Indicator.objects.all()
        last_full_year = Data_from_2007_2.objects.values_list('anio', 'trimestre').distinct().last()
        numqueries = 0

        for ind in indicators:
            for represent in xrange(1, 4):
                for method in xrange(1, 3):
                    if(method == 1):
                        if(ind.id == 8 or ind.id == 13 or ind.id == 20 or ind.id == 21 or ind.id == 33 or ind.id == 34 or ind.id == 35 or ind.id == 36 or ind.id == 37 or ind.id == 38):
                            break
                        data_ENEMDU_aux = Data_from_2003_4
                        yearStart_int = 2003
                        trimStart_int = 4
                        yearEnd_int = 2005
                        trimEnd_int = 4
                    else:
                        if(ind.id == 14 or ind.id == 15 or ind.id == 16 or ind.id == 17 or ind.id == 18):
                            break
                        data_ENEMDU_aux = Data_from_2007_2
                        yearStart_int = 2007
                        trimStart_int = 2
                        yearEnd_int = 2007
                        trimEnd_int = 2
                        yearEnd_int = last_full_year[0]
                        trimEnd_int = last_full_year[1]

                    trimStart_aux1 = trimStart_int
                    trimEnd_aux1 = trimStart_int

                    for yearStart_aux in xrange(yearStart_int, yearEnd_int+1):

                        if yearStart_aux == yearEnd_int:
                            trimStart_aux2 = trimEnd_int + 1
                        else:
                            trimStart_aux2 = 5

                        for trimStart_aux in xrange(trimStart_aux1, trimStart_aux2):

                            trimEnd_aux1 = trimStart_aux

                            for yearEnd_aux in xrange(yearStart_aux, yearEnd_int+1):

                                if yearEnd_aux == yearEnd_int:
                                    trimEnd_aux2 = trimEnd_int + 1
                                else:
                                    trimEnd_aux2 = 5

                                for trimEnd_aux in xrange(trimEnd_aux1, trimEnd_aux2):

                                    for num_disintegration in xrange(0, 3):

                                        if num_disintegration == 0:
                                            numqueries += 1
                                            disintegrations = []
                                            cache_value = '%s_%s_%s_%s_%s_%s_%s'%(ind.id, represent, method, yearStart_aux, trimStart_aux, yearEnd_aux, trimEnd_aux)
                                            data_ENEMDU = data_ENEMDU_aux.objects.all()
                                            if data_result is None:
                                                calc_data(ind.id, data_ENEMDU, yearStart_int, yearEnd_int, trimStart_int, trimEnd_int, yearStart_aux, yearEnd_aux, trimStart_aux, trimEnd_aux, represent, method, disintegrations, cache_value)
                                            # print ind.id, yearStart_aux, trimStart_aux, yearEnd_aux, trimEnd_aux, disintegrations

                                        elif num_disintegration == 1:
                                            for dis in indicator_filter_list(ind.id):
                                                numqueries += 1
                                                disintegrations = [dis]
                                                cache_value = '%s_%s_%s_%s_%s_%s_%s_%s'%(ind.id, represent, method, yearStart_aux, trimStart_aux, yearEnd_aux, trimEnd_aux, disintegrations[0])
                                                if(int(disintegrations[0]) == 2):
                                                    data_ENEMDU = get_data_by_represent(data_ENEMDU_aux, represent)
                                                else:
                                                    data_ENEMDU = data_ENEMDU_aux.objects.all()
                                                data_result = cache.get(cache_value)
                                                if data_result is None:
                                                    calc_data(ind.id, data_ENEMDU, yearStart_int, yearEnd_int, trimStart_int, trimEnd_int, yearStart_aux, yearEnd_aux, trimStart_aux, trimEnd_aux, represent, method, disintegrations, cache_value)
                                                    print ind.id, yearStart_aux, trimStart_aux, '-' , yearEnd_aux, trimEnd_aux, dis, disintegrations

                                        elif num_disintegration == 2:
                                            for dis1 in indicator_filter_list(ind.id):
                                                disintegration_accept_list = set(indicator_filter_list(ind.id)) - set(disintegration_denied_list(dis1)) - set([dis1])
                                                for dis2 in disintegration_accept_list:
                                                    numqueries += 1
                                                    disintegrations = [dis1, dis2]
                                                    cache_value = '%s_%s_%s_%s_%s_%s_%s_%s_%s'%(ind.id, represent, method, yearStart_aux, trimStart_aux, yearEnd_aux, trimEnd_aux, disintegrations[0], disintegrations[1])
                                                    if(int(disintegrations[0]) == 2 or int(disintegrations[1]) == 2):
                                                        data_ENEMDU = get_data_by_represent(data_ENEMDU_aux, represent)
                                                    else:
                                                        data_ENEMDU = data_ENEMDU_aux.objects.all()
                                                    data_result = cache.get(cache_value)
                                                    if data_result is None:
                                                        calc_data(ind.id, data_ENEMDU, yearStart_int, yearEnd_int, trimStart_int, trimEnd_int, yearStart_aux, yearEnd_aux, trimStart_aux, trimEnd_aux, represent, method, disintegrations, cache_value)
                                                    # print ind.id, yearStart_aux, trimStart_aux, yearEnd_aux, trimEnd_aux, dis1, dis2, disintegration_accept_list

                                if trimEnd_aux == 4:
                                    trimEnd_aux1 = 1
                        if trimStart_aux == 4:
                            trimStart_aux1 = 1
    message = json.dumps(1)
    return HttpResponse(message, content_type='application/json')


def total_consultas(request):
    user = request.user
    is_super_user = user.is_superuser

    if is_super_user:
        data_result = []
        indicators = Indicator.objects.all()
        represent = 2
        last_full_year = Data_from_2007_2.objects.values_list('anio', 'trimestre').distinct().last()
        numqueries = 0

        for ind in indicators:
            for represent in xrange(1, 4):
                for method in xrange(1, 3):
                    if(method == 1):
                        if(ind.id == 8 or ind.id == 13 or ind.id == 20 or ind.id == 21 or ind.id == 33 or ind.id == 34 or ind.id == 35 or ind.id == 36 or ind.id == 37 or ind.id == 38):
                            break
                        data_ENEMDU_aux = Data_from_2003_4
                        yearStart_int = 2004
                        trimStart_int = 1
                        yearEnd_int = 2004
                        trimEnd_int = 1
                    else:
                        if(ind.id == 14 or ind.id == 15 or ind.id == 16 or ind.id == 17 or ind.id == 18):
                            break
                        data_ENEMDU_aux = Data_from_2007_2
                        yearStart_int = 2007
                        trimStart_int = 2
                        yearEnd_int = 2007
                        trimEnd_int = 2
                        yearEnd_int = last_full_year[0]
                        trimEnd_int = last_full_year[1]

                    trimStart_aux1 = trimStart_int
                    trimEnd_aux1 = trimStart_int

                    for yearStart_aux in xrange(yearStart_int, yearEnd_int+1):

                        if yearStart_aux == yearEnd_int:
                            trimStart_aux2 = trimEnd_int + 1
                        else:
                            trimStart_aux2 = 5

                        for trimStart_aux in xrange(trimStart_aux1, trimStart_aux2):

                            trimEnd_aux1 = trimStart_aux

                            for yearEnd_aux in xrange(yearStart_aux, yearEnd_int+1):

                                if yearEnd_aux == yearEnd_int:
                                    trimEnd_aux2 = trimEnd_int + 1
                                else:
                                    trimEnd_aux2 = 5

                                for trimEnd_aux in xrange(trimEnd_aux1, trimEnd_aux2):

                                    for num_disintegration in xrange(0, 3):

                                        if num_disintegration == 0:
                                                numqueries += 1
                                                print numqueries
                                        elif num_disintegration == 1:
                                            for dis in indicator_filter_list(ind.id):
                                                numqueries += 1
                                                print numqueries
                                        elif num_disintegration == 2:
                                            for dis1 in indicator_filter_list(ind.id):
                                                disintegration_accept_list = set(indicator_filter_list(ind.id)) - set(disintegration_denied_list(dis1)) - set([dis1])
                                                for dis2 in disintegration_accept_list:
                                                   numqueries += 1
                                                   print numqueries

                                if trimEnd_aux == 4:
                                    trimEnd_aux1 = 1
                        if trimStart_aux == 4:
                            trimStart_aux1 = 1
        print numqueries
    message = json.dumps(numqueries)
    return HttpResponse(message, content_type='application/json')


def cache_page(request):
    template = "indicator_cache.html"
    return render_to_response(template, context_instance=RequestContext(request, locals()))


def access_denied(request):
    template = 'access_denied.html'
    return render_to_response(template, context_instance=RequestContext(request, locals()))