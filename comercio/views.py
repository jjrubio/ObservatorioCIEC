#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.shortcuts import HttpResponse, HttpResponseRedirect, render_to_response
from django.template.context import RequestContext
from django.template.loader import get_template
from models import *
import json
from django.core import serializers
from json import JSONEncoder
import pickle
from django.db.models import Q
from django.contrib import messages
from .forms import UploadFileForm
import csv
import os
import subprocess
import xlrd
from os import listdir
from os.path import isfile, join
from django.db import connection

class PythonObjectEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (list, dict, str, unicode, int, float, bool, type(None))):
            return JSONEncoder.default(self, obj)
        return {'_python_object': pickle.dumps(obj)}


def as_python_object(dct):
    if '_python_object' in dct:
        return pickle.loads(str(dct['_python_object']))
    return dct


def comercio_page(request):
    paises = Paises.objects.all()
    template = 'comercio.html'
    return render_to_response(template, context_instance = RequestContext(request,locals()))


def comercio(request):
    tipo = request.GET['tipo'].encode('ascii','ignore')
    option = request.GET['option'].encode('ascii','ignore')
    search_by = request.GET['search_by'].encode('ascii','ignore')
    standar = request.GET['standar'].encode('ascii','ignore')
    txt_desde = request.GET['txt_desde'].encode('ascii','ignore').replace('/', '-')+'-01'
    txt_hasta = request.GET['txt_hasta'].encode('ascii','ignore').replace('/', '-')+'-01'
    period = request.GET['period'].encode('ascii','ignore')
    txt_agregacion = request.GET['txt_agregacion'].encode('ascii','ignore')
    txt_patron = request.GET['txt_patron'].encode('ascii','ignore')
    checkbox_pais = request.GET['checkbox_pais'].encode('ascii','ignore')

    data_result = []
    data_table_A = []

    if option == '1':
        if search_by == '1':
            value_A = txt_patron+'%'
            value_B = None
        else:
            value_A = None
            value_B = '%'+txt_patron+'%'
    else:
        value_A = None
        value_B = '%'+txt_patron+'%'

    if standar == '1':
        standar_clase = 'subpartida'
        standar_var1 = 'subpartida_nandina'
        standar_var2 = 'subpartida_key'
        standar_table = 'comercio_nandina'
        export_standar_table = 'comercio_export_nandina'
        import_standar_table = 'comercio_import_nandina'
    else:
        standar_clase = standar_var1 = standar_var2 = 'codigo'
        if standar == '2':
            standar_table = 'comercio_cgce'
            export_standar_table = 'comercio_export_cgce'
            import_standar_table = 'comercio_import_cgce'
        elif standar == '3':
            standar_table = 'comercio_ciiu3'
            export_standar_table = 'comercio_export_ciiu3'
            import_standar_table = 'comercio_import_ciiu3'
        elif standar == '4':
            standar_table = 'comercio_cpc'
            export_standar_table = 'comercio_export_cpc'
            import_standar_table = 'comercio_import_cpc'
        elif standar == '5':
            standar_table = 'comercio_cuode'
            export_standar_table = 'comercio_export_cuode'
            import_standar_table = 'comercio_import_cuode'

    table_A = sql_A(option, standar_table, standar_clase, standar_var2, export_standar_table, value_A, value_B)

    for va in table_A:
        data_table_A.append([va[1], va[2]])

    data_result.append([data_table_A])


    data_table_B = []

    if option == '1':
        agreg = txt_agregacion
    else:
        value = txt_patron+'%'
        agreg = txt_agregacion

    if period == '4':
        ini_date = txt_desde[0:4]
        fin_date = txt_hasta[0:4]
    else:
        ini_date = txt_desde
        fin_date = txt_hasta

    if tipo == '1':
        tipo_standar_table = export_standar_table
    else:
        tipo_standar_table = import_standar_table

    if option == '1':
        table_B = sql_B_clase(tipo, tipo_standar_table, standar_table, standar_clase, standar_var1, standar_var2,
                                          period, value_A, value_B, agreg, ini_date, fin_date, checkbox_pais)

    else:
        table_B = sql_B_pais(tipo, tipo_standar_table, standar_table, standar_clase,
                                        standar_var1, standar_var2, period, value, agreg, ini_date, fin_date)

    totalPeso = 0
    totalFOB = 0
    totalCIF = 0

    if option == '1' and checkbox_pais == '0':
        if tipo == '1':
            for vb in table_B:
                totalPeso = totalPeso + float(vb[3])
                totalFOB = totalFOB + float(vb[4])
                data_table_B.append([vb[1], vb[2], float(vb[3]), float(vb[4])])
        else:
            for vb in table_B:
                totalPeso = totalPeso + float(vb[3])
                totalFOB = totalFOB + float(vb[4])
                totalCIF = totalCIF + float(vb[5])
                data_table_B.append([vb[1], vb[2], float(vb[3]), float(vb[4]), float(vb[5])])

    if (option == '1' and checkbox_pais == '1') or option == '2':
        if tipo == '1':
            for vb in table_B:
                totalPeso = totalPeso + float(vb[4])
                totalFOB = totalFOB + float(vb[5])
                data_table_B.append([vb[1], vb[2], vb[3], float(vb[4]), float(vb[5])])
        else:
            for vb in table_B:
                totalPeso = totalPeso + float(vb[4])
                totalFOB = totalFOB + float(vb[5])
                totalCIF = totalCIF + float(vb[6])
                data_table_B.append([vb[1], vb[2], vb[3], float(vb[4]), float(vb[5]), float(vb[6])])

    data_result.append([data_table_B])

    if(tipo == 1):
        data_result.append([totalPeso, totalFOB])
    else:
        data_result.append([totalPeso, totalFOB, totalCIF])

    message = json.dumps(data_result, cls=PythonObjectEncoder)
    return HttpResponse(message, content_type='application/json')

def equivalencia(value):
    estandar = ['cgce', 'ciiu3', 'cpc', 'cuode']
    tabla_trans_nandina = ['comercio_export_nandina', 'comercio_import_nandina']
    tabla_trans_estandar = ['comercio_export_cgce', 'comercio_export_ciiu3', 'comercio_export_cpc', 'comercio_export_cuode',
                                           'comercio_import_cgce', 'comercio_import_ciiu3', 'comercio_import_cpc', 'comercio_import_cuode']

    j = 0
    k = value

    if k == 0:
        c=0
    else:
        c=4

    bandera = 0

    for i in xrange(c, len(tabla_trans_estandar)):
        if bandera == 4:
            break
        else:
            if k == 0:
                raw_body = ("""INSERT INTO %s (ANO, MES, PAIS, CODIGO, PESO, FOB)
                                        SELECT ANO, MES, PAIS, CODIGO, PESO, FOB
                                        FROM
                                        (SELECT id, ano AS ANO,
                                        mes AS MES,
                                        pais AS PAIS,
                                        codigo AS CODIGO,
                                        peso AS PESO,
                                        fob AS FOB
                                        FROM(
                                        SELECT nandina AS SUBPARTIDA,
                                        %s AS CODIGO
                                        FROM comercio_equivalencia)
                                        AS MATCH_TABLE
                                        INNER JOIN %s ON
                                        (MATCH_TABLE.SUBPARTIDA = %s.subpartida_key)) AS VIEW
                                    """) % (tabla_trans_estandar[i], estandar[j], tabla_trans_nandina[k], tabla_trans_nandina[k])
            else:
                raw_body = ("""INSERT INTO %s (ANO, MES, PAIS, CODIGO, PESO, FOB, CIF)
                                        SELECT ANO, MES, PAIS, CODIGO, PESO, FOB, CIF
                                        FROM
                                        (SELECT id, ano AS ANO,
                                        mes AS MES,
                                        pais AS PAIS,
                                        codigo AS CODIGO,
                                        peso AS PESO,
                                        fob AS FOB,
                                        cif AS CIF
                                        FROM(
                                        SELECT nandina AS SUBPARTIDA,
                                        %s AS CODIGO
                                        FROM comercio_equivalencia)
                                        AS MATCH_TABLE
                                        INNER JOIN %s ON
                                        (MATCH_TABLE.SUBPARTIDA = %s.subpartida_key)) AS VIEW
                                    """) % (tabla_trans_estandar[i], estandar[j], tabla_trans_nandina[k], tabla_trans_nandina[k])

        j = j + 1

        bandera = bandera + 1

        cursor = connection.cursor()
        cursor.execute(raw_body)
        cursor.close

    return 1

#standar_table: comercio_nandina, comercio_cgce, comercio_cpc, comercio_cuode, comercio_ciiu3 (nombre propio de la base)
#standar_clase: subpartida o codigo
#value_A: patron% o null segun 'BuscarPor'
#value_B: patron% o null segun 'BuscarPor'
def sql_A(option, standar_table, standar_clase, standar_var2, export_standar_table, value_A, value_B):
    cursor = connection.cursor()

    if(option == '1'):
        raw_body = ("SELECT * FROM %s WHERE %s ") % (standar_table, standar_clase)
        raw_where = ("LIKE %s OR descripcion LIKE %s")
        cursor.execute(raw_body+raw_where,  [value_A, value_B])
        table_A = cursor.fetchall ()
        return table_A
    else:
        raw_body = ("""SELECT DISTINCT %s.id, %s.%s, descripcion 
                                FROM %s
                                INNER JOIN %s ON %s.%s=%s.%s 
                                INNER JOIN comercio_paises ON %s.pais=comercio_paises.codigo 
                                WHERE comercio_paises.pais """) % (standar_table, export_standar_table, standar_var2, 
                                                                                       export_standar_table, 
                                                                                       standar_table, export_standar_table, standar_var2, standar_table, standar_clase, 
                                                                                       export_standar_table)
        raw_where = ("LIKE %s")
        cursor.execute(raw_body + raw_where, [value_B])
        table_A = cursor.fetchall ()
        return table_A


#tipo: tab_selected
#standar_table: comercio_nandina, comercio_cgce, comercio_cpc, comercio_cuode, comercio_ciiu3 (nombre propio de la base)
#standar_clase: subpartida o codigo
#periodicidad: mes, trimestre, semestre, anual
#value_A: patron% o null segun 'BuscarPor'
#value_B: patron% o null segun 'BuscarPor'
#agreg: # nivel de agregacion
#ini_date: desde.substring(0,4)
#fin_date: hasta.substring(0,4)
#checkbox_pais: si se separa por pais o no
def sql_B_clase(tipo, tipo_standar_table, standar_table, standar_clase, standar_var1, standar_var2,
                        period, value_A, value_B, agreg, ini_date, fin_date, checkbox_pais):

    cursor = connection.cursor()

    #subpartida/codigo por mes
    if period == '1':
        if checkbox_pais == '0':
            if tipo == '1':
                raw_body_1 = ("""SELECT id, substr(ifnull(date(concat(ANO,'-0',MES,'-01')),date(concat(ANO,'-',MES,'-01'))),1,7) AS FECHA,
                                        substr(%s,1,%s) AS %s,
                                        sum(peso) AS PESO,
                                        sum(fob) AS SUBTOTAL_FOB
                                        """) % (standar_var1, agreg, standar_clase)
            else:
                raw_body_1 = ("""SELECT id, substr(ifnull(date(concat(ANO,'-0',MES,'-01')),date(concat(ANO,'-',MES,'-01'))),1,7) AS FECHA,
                                        substr(%s,1,%s) AS %s,
                                        sum(peso) AS PESO,
                                        sum(fob) AS SUBTOTAL_FOB,
                                        sum(cif) AS SUBTOTAL_CIF
                                        """) % (standar_var1, agreg, standar_clase)

            raw_body_2 = ("""FROM %s
                                        WHERE (%s IN
                                        (SELECT %s
                                        FROM %s
                                        WHERE (%s
                                    """) % (tipo_standar_table, standar_var2, standar_clase, standar_table, standar_clase)

            raw_where_1 = ("LIKE %s) OR (descripcion LIKE %s))) GROUP BY ANO, MES,")

            raw_body_3 = ("substr(%s,1,%s)") % (standar_var1, agreg)

            raw_where_2 = ("HAVING (substr(ifnull(date(concat(ANO,'-0',MES,'-01')),date(concat(ANO,'-',MES,'-01'))),1,7)>=%s) AND (substr(ifnull(date(concat(ANO,'-0',MES,'-01')),date(concat(ANO,'-',MES,'-01'))),1,7)<=%s)")

        else:
            if tipo == '1':
                raw_body_1 = ("""SELECT %s.id, substr(ifnull(date(concat(ANO,'-0',MES,'-01')),date(concat(ANO,'-',MES,'-01'))),1,7) AS FECHA,
                                        comercio_paises.pais AS PAIS,
                                        substr(%s.%s,1,%s) AS %s,
                                        sum(peso) AS PESO,
                                        sum(fob) AS SUBTOTAL_FOB
                                        """) % (tipo_standar_table, tipo_standar_table, standar_var1, agreg, standar_clase)
            else:
                raw_body_1 = ("""SELECT %s.id, substr(ifnull(date(concat(ANO,'-0',MES,'-01')),date(concat(ANO,'-',MES,'-01'))),1,7) AS FECHA,
                                        comercio_paises.pais AS PAIS,
                                        substr(%s.%s,1,%s) AS %s,
                                        sum(peso) AS PESO,
                                        sum(fob) AS SUBTOTAL_FOB,
                                        sum(cif) AS SUBTOTAL_CIF
                                        """) % (tipo_standar_table, tipo_standar_table, standar_var1, agreg, standar_clase)

            raw_body_2 = ("""FROM %s
                                    INNER JOIN comercio_paises ON %s.pais=comercio_paises.codigo
                                    WHERE (%s.%s IN
                                    (SELECT %s FROM %s WHERE (%s
                                    """) % (tipo_standar_table, tipo_standar_table, tipo_standar_table, standar_var2, standar_clase, standar_table, standar_clase)

            raw_where_1 = ("LIKE %s) OR (descripcion LIKE %s))) ")

            raw_body_3 = ("GROUP BY ano, mes, substr(%s.%s,1,%s),%s.pais ") % (tipo_standar_table, standar_var1, agreg, tipo_standar_table)

            raw_where_2 = ("HAVING (substr(ifnull(date(concat(ANO,'-0',MES,'-01')),date(concat(ANO,'-',MES,'-01'))),1,7)>=%s) AND (substr(ifnull(date(concat(ANO,'-0',MES,'-01')),date(concat(ANO,'-',MES,'-01'))),1,7)<=%s)")

    #subpartida/codigo por trimestre
    elif period == '2':
        if checkbox_pais == '0':
            if tipo == '1':
                raw_body_1 = ("""SELECT V_TABLE.id,
                                        concat(ANO,'-0',FLOOR(SEMESTRE)) AS FECHA,
                                        V_TABLE.%s AS %s,
                                        V_TABLE.PESO AS PESO,
                                        V_TABLE.SUBTOTAL_FOB AS SUBTOTAL_FOB
                                        FROM( SELECT id, ano AS ANO, ((MES-1)/3)+1 AS SEMESTRE,
                                        substr(%s,1,%s) AS %s,
                                        sum(peso) AS PESO,
                                        sum(fob) AS SUBTOTAL_FOB
                                       """) % (standar_clase, standar_clase, standar_var1, agreg, standar_clase)
            else:
                raw_body_1 = ("""SELECT V_TABLE.id,
                                        concat(ANO,'-0',FLOOR(SEMESTRE)) AS FECHA,
                                        V_TABLE.%s AS %s,
                                        V_TABLE.PESO AS PESO,
                                        V_TABLE.SUBTOTAL_FOB AS SUBTOTAL_FOB,
                                        V_TABLE.SUBTOTAL_CIF AS SUBTOTAL_CIF
                                        FROM( SELECT id, ano AS ANO, ((MES-1)/3)+1 AS SEMESTRE,
                                        substr(%s,1,%s) AS %s,
                                        sum(peso) AS PESO,
                                        sum(fob) AS SUBTOTAL_FOB,
                                        sum(cif) AS SUBTOTAL_CIF
                                       """) % (standar_clase, standar_clase, standar_var1, agreg, standar_clase)

            raw_body_2 = ("""FROM %s
                                        WHERE (%s IN
                                        (SELECT %s
                                        FROM %s
                                        WHERE (%s
                                    """) % (tipo_standar_table, standar_var2, standar_clase, standar_table, standar_clase)

            raw_where_1 = ("LIKE %s) OR (descripcion LIKE %s))) ")

            raw_body_3 = ("GROUP BY ANO, SEMESTRE, substr(%s.%s,1,%s)) AS V_TABLE ") % (tipo_standar_table, standar_var1, agreg)

            raw_where_2 = ("WHERE (concat(ANO,'-0',FLOOR(SEMESTRE))>=%s) AND (concat(ANO,'-0',FLOOR(SEMESTRE))<=%s)")

        else:
            if tipo == '1':
                raw_body_1 = ("""SELECT id, concat(ANO,'-0',FLOOR(SEMESTRE)) AS FECHA,
                                        V_TABLE.pais AS PAIS,
                                        V_TABLE.%s AS %s,
                                        V_TABLE.PESO AS PESO,
                                        V_TABLE.SUBTOTAL_FOB AS SUBTOTAL_FOB
                                        FROM( SELECT comercio_paises.id, ano AS ANO, ((MES-1)/3)+1 AS SEMESTRE,
                                        comercio_paises.pais AS PAIS,
                                        substr(%s.%s,1,%s) AS %s,
                                        sum(peso) AS PESO,
                                        sum(fob) AS SUBTOTAL_FOB
                                       """) % (standar_clase, standar_clase, tipo_standar_table, standar_var1, agreg, standar_clase)
            else:
                raw_body_1 = ("""SELECT id, concat(ANO,'-0',FLOOR(SEMESTRE)) AS FECHA,
                                        V_TABLE.pais AS PAIS,
                                        V_TABLE.%s AS %s,
                                        V_TABLE.PESO AS PESO,
                                        V_TABLE.SUBTOTAL_FOB AS SUBTOTAL_FOB,
                                        V_TABLE.SUBTOTAL_CIF AS SUBTOTAL_CIF
                                        FROM( SELECT comercio_paises.id, ano AS ANO, ((MES-1)/3)+1 AS SEMESTRE,
                                        comercio_paises.pais AS PAIS,
                                        substr(%s.%s,1,%s) AS %s,
                                        sum(peso) AS PESO,
                                        sum(fob) AS SUBTOTAL_FOB,
                                        sum(cif) AS SUBTOTAL_CIF

                                       """) % (standar_clase, standar_clase, tipo_standar_table, standar_var1, agreg, standar_clase)

            raw_body_2 = ("""FROM %s
                                    INNER JOIN comercio_paises ON %s.pais=comercio_paises.codigo
                                    WHERE (%s.%s IN
                                    (SELECT %s FROM %s WHERE (%s
                                    """) % (tipo_standar_table, tipo_standar_table, tipo_standar_table, standar_var2, standar_clase, standar_table, standar_clase)

            raw_where_1 = ("LIKE %s) OR (descripcion LIKE %s))) ")

            raw_body_3 = ("GROUP BY ANO, SEMESTRE,substr(%s.%s,1,%s),%s.pais) AS V_TABLE ") % (tipo_standar_table, standar_var1, agreg, tipo_standar_table)

            raw_where_2 = ("WHERE (concat(ANO,'-0',FLOOR(SEMESTRE))>=%s) AND (concat(ANO,'-0',FLOOR(SEMESTRE))<=%s)")

    #subpartida/codigo por semestre
    elif period == '3':
        if checkbox_pais == '0':
            if tipo == '1':
                raw_body_1 = ("""SELECT V_TABLE.id,
                                        concat(ANO,'-0',FLOOR(SEMESTRE)) AS FECHA,
                                        V_TABLE.%s AS %s,
                                        V_TABLE.PESO AS PESO,
                                        V_TABLE.SUBTOTAL_FOB AS SUBTOTAL_FOB
                                        FROM( SELECT id, ano AS ANO, ((MES-1)/6)+1 AS SEMESTRE,
                                        substr(%s,1,%s) AS %s,
                                        sum(peso) AS PESO,
                                        sum(fob) AS SUBTOTAL_FOB
                                       """) % (standar_clase, standar_clase, standar_var1, agreg, standar_clase)
            else:
                raw_body_1 = ("""SELECT V_TABLE.id,
                                        concat(ANO,'-0',FLOOR(SEMESTRE)) AS FECHA,
                                        V_TABLE.%s AS %s,
                                        V_TABLE.PESO AS PESO,
                                        V_TABLE.SUBTOTAL_FOB AS SUBTOTAL_FOB,
                                        V_TABLE.SUBTOTAL_CIF AS SUBTOTAL_CIF
                                        FROM( SELECT id, ano AS ANO, ((MES-1)/6)+1 AS SEMESTRE,
                                        substr(%s,1,%s) AS %s,
                                        sum(peso) AS PESO,
                                        sum(fob) AS SUBTOTAL_FOB,
                                        sum(cif) AS SUBTOTAL_CIF
                                       """) % (standar_clase, standar_clase, standar_var1, agreg, standar_clase)

            raw_body_2 = ("""FROM %s
                                        WHERE (%s IN
                                        (SELECT %s
                                        FROM %s
                                        WHERE (%s
                                    """) % (tipo_standar_table, standar_var2, standar_clase, standar_table, standar_clase)

            raw_where_1 = ("LIKE %s) OR (descripcion LIKE %s))) ")

            raw_body_3 = ("GROUP BY ANO, SEMESTRE, substr(%s.%s,1,%s)) AS V_TABLE ") % (tipo_standar_table, standar_var1, agreg)

            raw_where_2 = ("WHERE (concat(ANO,'-0',FLOOR(SEMESTRE))>=%s) AND (concat(ANO,'-0',FLOOR(SEMESTRE))<=%s)")

        else:
            if tipo == '1':
                raw_body_1 = ("""SELECT id, concat(ANO,'-0',FLOOR(SEMESTRE)) AS FECHA,
                                        V_TABLE.pais AS PAIS,
                                        V_TABLE.%s AS %s,
                                        V_TABLE.PESO AS PESO,
                                        V_TABLE.SUBTOTAL_FOB AS SUBTOTAL_FOB
                                        FROM( SELECT comercio_paises.id, ano AS ANO, ((MES-1)/6)+1 AS SEMESTRE,
                                        comercio_paises.pais AS PAIS,
                                        substr(%s.%s,1,%s) AS %s,
                                        sum(peso) AS PESO,
                                        sum(fob) AS SUBTOTAL_FOB
                                       """) % (standar_clase, standar_clase, tipo_standar_table, standar_var1, agreg, standar_clase)
            else:
                raw_body_1 = ("""SELECT id, concat(ANO,'-0',FLOOR(SEMESTRE)) AS FECHA,
                                        V_TABLE.pais AS PAIS,
                                        V_TABLE.%s AS %s,
                                        V_TABLE.PESO AS PESO,
                                        V_TABLE.SUBTOTAL_FOB AS SUBTOTAL_FOB,
                                        V_TABLE.SUBTOTAL_CIF AS SUBTOTAL_CIF
                                        FROM( SELECT comercio_paises.id, ano AS ANO, ((MES-1)/6)+1 AS SEMESTRE,
                                        comercio_paises.pais AS PAIS,
                                        substr(%s.%s,1,%s) AS %s,
                                        sum(peso) AS PESO,
                                        sum(fob) AS SUBTOTAL_FOB,
                                        sum(cif) AS SUBTOTAL_CIF

                                       """) % (standar_clase, standar_clase, tipo_standar_table, standar_var1, agreg, standar_clase)

            raw_body_2 = ("""FROM %s
                                    INNER JOIN comercio_paises ON %s.pais=comercio_paises.codigo
                                    WHERE (%s.%s IN
                                    (SELECT %s FROM %s WHERE (%s
                                    """) % (tipo_standar_table, tipo_standar_table, tipo_standar_table, standar_var2, standar_clase, standar_table, standar_clase)

            raw_where_1 = ("LIKE %s) OR (descripcion LIKE %s))) ")

            raw_body_3 = ("GROUP BY ANO, SEMESTRE,substr(%s.%s,1,%s),%s.pais) AS V_TABLE ") % (tipo_standar_table, standar_var1, agreg, tipo_standar_table)

            raw_where_2 = ("WHERE (concat(ANO,'-0',FLOOR(SEMESTRE))>=%s) AND (concat(ANO,'-0',FLOOR(SEMESTRE))<=%s)")

    #subpartida/codigo por anio
    elif period == '4':
        if checkbox_pais == '0':
            if tipo == '1':
                raw_body_1 = ("""SELECT id, ano AS ANO,
                                        substr(%s,1,%s) AS %s,
                                        sum(peso) AS PESO,
                                        sum(fob) AS SUBTOTAL_FOB
                                       """) % (standar_var1, agreg, standar_clase)
            else:
                raw_body_1 = ("""SELECT id, ano AS ANO,
                                        substr(%s,1,%s) AS %s,
                                        sum(peso) AS PESO,
                                        sum(fob) AS SUBTOTAL_FOB,
                                        sum(cif) AS SUBTOTAL_CIF
                                       """) % (standar_var1, agreg, standar_clase)

            raw_body_2 = ("""FROM %s
                                    WHERE (%s IN
                                    (SELECT %s FROM %s WHERE (%s
                                    """) % (tipo_standar_table, standar_var2, standar_clase, standar_table, standar_clase)

            raw_where_1 = ("LIKE %s) OR (descripcion LIKE %s))) ")

            raw_body_3 = ("GROUP BY ano, substr(%s.%s,1,%s) ") % (tipo_standar_table, standar_var1, agreg)

            raw_where_2 = ("HAVING (ANO>=%s) AND (ANO<=%s)")

        else:
            if tipo == '1':
                raw_body_1 = ("""SELECT %s.id, ano AS ANO,
                                        comercio_paises.pais AS PAIS,
                                        substr(%s.%s,1,%s) AS %s,
                                        sum(peso) AS PESO,
                                        sum(fob) AS SUBTOTAL_FOB
                                       """) % (tipo_standar_table, tipo_standar_table, standar_var1, agreg, standar_clase)
            else:
                raw_body_1 = ("""SELECT %s.id, ano AS ANO,
                                        comercio_paises.pais AS PAIS,
                                        substr(%s.%s,1,%s) AS %s,
                                        sum(peso) AS PESO,
                                        sum(fob) AS SUBTOTAL_FOB,
                                        sum(cif) AS SUBTOTAL_CIF
                                       """) % (tipo_standar_table, tipo_standar_table, standar_var1, agreg, standar_clase)

            raw_body_2 = ("""FROM %s
                                    INNER JOIN comercio_paises ON %s.pais=comercio_paises.codigo
                                    WHERE (%s.%s IN
                                    (SELECT %s FROM %s WHERE (%s
                                    """) % (tipo_standar_table, tipo_standar_table, tipo_standar_table, standar_var2, standar_clase, standar_table, standar_clase)

            raw_where_1 = ("LIKE %s) OR (descripcion LIKE %s))) ")

            raw_body_3 = ("GROUP BY %s.ano,substr(%s.%s,1,%s),%s.pais ") % (tipo_standar_table, tipo_standar_table, standar_var1, agreg, tipo_standar_table)

            raw_where_2 = ("HAVING (ANO>=%s) AND (ANO<=%s)")

    cursor.execute(raw_body_1 + raw_body_2 + raw_where_1 + raw_body_3 + raw_where_2, [value_A, value_B, ini_date, fin_date])

    table_B = cursor.fetchall ()

    return table_B


def sql_B_pais(tipo, tipo_standar_table, standar_table, standar_clase,
                      standar_var1, standar_var2, period, value, agreg, ini_date, fin_date):

    cursor = connection.cursor()

    #pais por mes
    if period == '1':
        if tipo == '1':
            raw_body_1 = ("""SELECT %s.id, substr(ifnull(date(concat(ANO,'-0',MES,'-01')),date(concat(ANO,'-',MES,'-01'))),1,7) AS FECHA,
                                    comercio_paises.pais AS PAIS,
                                    substr(%s.%s,1,%s) AS %s,
                                    sum(peso) AS PESO,
                                    sum(fob) AS SUBTOTAL_FOB
                                    """) % (tipo_standar_table, tipo_standar_table, standar_var1, agreg, standar_clase)
        else:
            raw_body_1 = ("""SELECT %s.id, substr(ifnull(date(concat(ANO,'-0',MES,'-01')),date(concat(ANO,'-',MES,'-01'))),1,7) AS FECHA,
                                    comercio_paises.pais AS PAIS,
                                    substr(%s.%s,1,%s) AS %s,
                                    sum(peso) AS PESO,
                                    sum(fob) AS SUBTOTAL_FOB,
                                    sum(cif) AS SUBTOTAL_CIF
                                    """) % (tipo_standar_table, tipo_standar_table, standar_var1, agreg, standar_clase)

        raw_body_2 = ("""FROM %s
                                INNER JOIN comercio_paises ON %s.pais=comercio_paises.codigo
                                WHERE (%s.pais IN
                                (SELECT codigo FROM comercio_paises WHERE (pais
                                """) % (tipo_standar_table, tipo_standar_table, tipo_standar_table)

        raw_where_1 = ("LIKE %s))) ")

        raw_body_3 = ("GROUP BY ano, mes, substr(%s.%s,1,%s),%s.pais ") % (tipo_standar_table, standar_var1, agreg, tipo_standar_table)

        raw_where_2 = ("HAVING (substr(ifnull(date(concat(ANO,'-0',MES,'-01')),date(concat(ANO,'-',MES,'-01'))),1,7)>=%s) AND (substr(ifnull(date(concat(ANO,'-0',MES,'-01')),date(concat(ANO,'-',MES,'-01'))),1,7)<=%s)")

    #pais por trimestre
    elif period == '2':
        if tipo == '1':
            raw_body_1 = ("""SELECT id, concat(ANO,'-0',FLOOR(SEMESTRE)) AS FECHA,
                                    V_TABLE.pais AS PAIS,
                                    V_TABLE.%s AS %s,
                                    V_TABLE.PESO AS PESO,
                                    V_TABLE.SUBTOTAL_FOB AS SUBTOTAL_FOB
                                    FROM( SELECT comercio_paises.id, ano AS ANO, ((MES-1)/3)+1 AS SEMESTRE,
                                    comercio_paises.pais AS PAIS,
                                    substr(%s.%s,1,%s) AS %s,
                                    sum(peso) AS PESO,
                                    sum(fob) AS SUBTOTAL_FOB
                                   """) % (standar_clase, standar_clase, tipo_standar_table, standar_var1, agreg, standar_clase)
        else:
            raw_body_1 = ("""SELECT id, concat(ANO,'-0',FLOOR(SEMESTRE)) AS FECHA,
                                    V_TABLE.pais AS PAIS,
                                    V_TABLE.%s AS %s,
                                    V_TABLE.PESO AS PESO,
                                    V_TABLE.SUBTOTAL_FOB AS SUBTOTAL_FOB,
                                    V_TABLE.SUBTOTAL_CIF AS SUBTOTAL_CIF
                                    FROM( SELECT comercio_paises.id, ano AS ANO, ((MES-1)/3)+1 AS SEMESTRE,
                                    comercio_paises.pais AS PAIS,
                                    substr(%s.%s,1,%s) AS %s,
                                    sum(peso) AS PESO,
                                    sum(fob) AS SUBTOTAL_FOB,
                                    sum(cif) AS SUBTOTAL_CIF

                                   """) % (standar_clase, standar_clase, tipo_standar_table, standar_var1, agreg, standar_clase)

        raw_body_2 = ("""FROM %s
                                INNER JOIN comercio_paises ON %s.pais=comercio_paises.codigo
                                WHERE (%s.pais IN
                                (SELECT codigo FROM comercio_paises WHERE (pais
                                """) % (tipo_standar_table, tipo_standar_table, tipo_standar_table)

        raw_where_1 = ("LIKE %s))) ")

        raw_body_3 = ("GROUP BY ANO, SEMESTRE,substr(%s.%s,1,%s),%s.pais) AS V_TABLE ") % (tipo_standar_table, standar_var1, agreg, tipo_standar_table)

        raw_where_2 = ("WHERE (concat(ANO,'-0',FLOOR(SEMESTRE))>=%s) AND (concat(ANO,'-0',FLOOR(SEMESTRE))<=%s)")

    #pais por semestre
    elif period == '3':
        if tipo == '1':
            raw_body_1 = ("""SELECT id, concat(ANO,'-0',FLOOR(SEMESTRE)) AS FECHA,
                                    V_TABLE.pais AS PAIS,
                                    V_TABLE.%s AS %s,
                                    V_TABLE.PESO AS PESO,
                                    V_TABLE.SUBTOTAL_FOB AS SUBTOTAL_FOB
                                    FROM( SELECT comercio_paises.id, ano AS ANO, ((MES-1)/6)+1 AS SEMESTRE,
                                    comercio_paises.pais AS PAIS,
                                    substr(%s.%s,1,%s) AS %s,
                                    sum(peso) AS PESO,
                                    sum(fob) AS SUBTOTAL_FOB
                                   """) % (standar_clase, standar_clase, tipo_standar_table, standar_var1, agreg, standar_clase)
        else:
            raw_body_1 = ("""SELECT id, concat(ANO,'-0',FLOOR(SEMESTRE)) AS FECHA,
                                    V_TABLE.pais AS PAIS,
                                    V_TABLE.%s AS %s,
                                    V_TABLE.PESO AS PESO,
                                    V_TABLE.SUBTOTAL_FOB AS SUBTOTAL_FOB.
                                    V_TABLE.SUBTOTAL_CIF AS SUBTOTAL_CIF
                                    FROM( SELECT comercio_paises.id, ano AS ANO, ((MES-1)/6)+1 AS SEMESTRE,
                                    comercio_paises.pais AS PAIS,
                                    substr(%s.%s,1,%s) AS %s,
                                    sum(peso) AS PESO,
                                    sum(fob) AS SUBTOTAL_FOB,
                                    sum(cif) AS SUBTOTAL_CIF

                                   """) % (standar_clase, standar_clase, tipo_standar_table, standar_var1, agreg, standar_clase)

        raw_body_2 = ("""FROM %s
                                INNER JOIN comercio_paises ON %s.pais=comercio_paises.codigo
                                WHERE (%s.pais IN
                                (SELECT codigo FROM comercio_paises WHERE (pais
                                """) % (tipo_standar_table, tipo_standar_table, tipo_standar_table)

        raw_where_1 = ("LIKE %s))) ")

        raw_body_3 = ("GROUP BY ANO, SEMESTRE,substr(%s.%s,1,%s),%s.pais) AS V_TABLE ") % (tipo_standar_table, standar_var1, agreg, tipo_standar_table)

        raw_where_2 = ("WHERE (concat(ANO,'-0',FLOOR(SEMESTRE))>=%s) AND (concat(ANO,'-0',FLOOR(SEMESTRE))<=%s)")

    #pais por anio
    elif period == '4':
        if tipo == '1':
            raw_body_1 = ("""SELECT %s.id, ano AS ANO,
                                    comercio_paises.pais AS PAIS,
                                    substr(%s.%s,1,%s) AS %s,
                                    sum(peso) AS PESO,
                                    sum(fob) AS SUBTOTAL_FOB
                                   """) % (tipo_standar_table, tipo_standar_table, standar_var1, agreg, standar_clase)
        else:
            raw_body_1 = ("""SELECT %s.id, ano AS ANO,
                                    comercio_paises.pais AS PAIS,
                                    substr(%s.%s,1,%s) AS %s,
                                    sum(peso) AS PESO,
                                    sum(fob) AS SUBTOTAL_FOB,
                                    sum(cif) AS SUBTOTAL_CIF
                                   """) % (tipo_standar_table, tipo_standar_table, standar_var1, agreg, standar_clase)

        raw_body_2 = ("""FROM %s
                                INNER JOIN comercio_paises ON comercio_paises.codigo=%s.pais
                                WHERE (%s.pais IN
                                (SELECT codigo FROM comercio_paises WHERE (pais
                                """) % (tipo_standar_table, tipo_standar_table, tipo_standar_table)

        raw_where_1 = ("LIKE %s))) ")

        raw_body_3 = ("GROUP BY %s.ano,substr(%s.%s,1,%s),%s.pais ") % (tipo_standar_table, tipo_standar_table, standar_var1, agreg, tipo_standar_table)

        raw_where_2 = ("HAVING (ANO>=%s) AND (ANO<=%s)")

    cursor.execute(raw_body_1 + raw_body_2 + raw_where_1 + raw_body_3 + raw_where_2, [value, ini_date, fin_date])

    table_B = cursor.fetchall ()

    return table_B

def insert_data_comercio(request):
    context = RequestContext(request)
    template = 'insert_data_comercio.html'
    upload_success = False
    empty = False
    arreglo = []
    path_dir = '/home/ciec/oese/media/csv/'
    user = request.user
    is_super_user = user.is_superuser
    coma = ','
    actualizar = False
    file_list = request.FILES.getlist('file')
    files_failed = []
    error_find = []

    
    file_list = request.FILES.getlist('file')
    user = request.user
    is_super_user = user.is_superuser
    if is_super_user:
        if request.method == 'POST':
            upload_form = UploadFileForm(request.POST, request.FILES)
            if 'file' in request.FILES:
                if upload_form.is_valid():
                    choices = upload_form.cleaned_data['choices']
                    if choices == '1':
                        dbtable = 'comercio_cgce'
                    elif choices == '2':
                        dbtable = 'comercio_ciiu3'
                    elif choices == '3':
                        dbtable = 'comercio_cpc'
                    elif choices == '4':
                        dbtable = 'comercio_cuode'
                    elif choices == '5':
                        dbtable = 'comercio_nandina'
                    elif choices == '6':
                        dbtable = 'comercio_paises'
                    elif choices == '7':
                        dbtable = 'comercio_equivalencia'
                    elif choices == '8':
                        dbtable = 'comercio_export_nandina'
                    elif choices == '9':
                        dbtable = 'comercio_import_nandina'
                    elif choices == '10':
                        dbtable = 'comercio_export_total'
                    else:
                        dbtable = 'comercio_import_total'
                    for afile in file_list:
                        var_split = str(afile)
                        extension = var_split.split('.',1)
                        ext_val = extension[1]
                        if ext_val == 'txt' or ext_val == 'csv':
                            pass
                        else:
                            return HttpResponseRedirect('/error-extension/')
                    for afile in file_list:
                        new_file_import = upload_csv_file(upload=afile)
                        new_file_import.save()
                    for afile in file_list:
                        file_name = afile
                        full_path_name = path_dir+str(file_name)
                        with open(str(full_path_name),'rb') as csvfile:
                            reader = csv.reader(csvfile)
                            my_list = list(reader)
                            if choices == '1':
                                for i in range(1,len(my_list)):
                                    codigo,descripcion = str(my_list[i]).split(';')
                                    codigo_new,value = codigo.split('[')
                                    value_coma,wcoma = value.split("'")
                                    descripcion_new = descripcion.split("]")
                                    try:
                                        codigo_int = int(wcoma)
                                    except ValueError:
                                        files_failed.append(str(afile))
                                        break
                                    try:
                                        descripcion_str = str(descripcion_new[0])
                                    except ValueError:
                                        files_failed.append(str(afile))
                                        break
                            elif choices == '2':
                                for i in range(1,len(my_list)):
                                    codigo,descripcion = str(my_list[i]).split(';')
                                    codigo_new,value = codigo.split('[')
                                    value_coma,wcoma = value.split("'")
                                    descripcion_new = descripcion.split("]")
                                    try:
                                        codigo_int = int(wcoma)
                                    except ValueError:
                                        files_failed.append(str(afile))
                                        break
                                    try:
                                        descripcion_str = str(descripcion_new[0])
                                    except ValueError:
                                        files_failed.append(str(afile))
                                        break
                            elif choices == '3':
                                for i in range(1,len(my_list)):
                                    codigo,descripcion = str(my_list[i]).split(';')
                                    codigo_new,value = codigo.split('[')
                                    value_coma,wcoma = value.split("'")
                                    descripcion_new = descripcion.split("]")
                                    try:
                                        codigo_int = int(wcoma)
                                    except ValueError:
                                        files_failed.append(str(afile))
                                        break
                                    try:
                                        descripcion_str = str(descripcion_new[0])
                                    except ValueError:
                                        files_failed.append(str(afile))
                                        break
                            elif choices == '4':
                                for i in range(1,len(my_list)):
                                    codigo,descripcion = str(my_list[i]).split(';')
                                    codigo_new,value = codigo.split('[')
                                    value_coma,wcoma = value.split("'")
                                    descripcion_new = descripcion.split("]")
                                    try:
                                        codigo_int = int(wcoma)
                                    except ValueError:
                                        files_failed.append(str(afile))
                                        break
                                    try:
                                        descripcion_str = str(descripcion_new[0])
                                    except ValueError:
                                        files_failed.append(str(afile))
                                        break
                            elif choices == '5':
                                for i in range(1,len(my_list)):
                                    subpartida,descripcion = str(my_list[i]).split(';')
                                    codigo_new,value = subpartida.split('[')
                                    value_coma,wcoma = value.split("'")
                                    descripcion_new = descripcion.split("]")
                                    try:
                                        codigo_int = int(wcoma)
                                    except ValueError:
                                        files_failed.append(str(afile))
                                        break
                                    try:
                                        descripcion_str = str(descripcion_new[0])
                                    except ValueError:
                                        files_failed.append(str(afile))
                                        break
                            elif choices == '6':
                                for i in range(1,len(my_list)):
                                    codigo,pais = str(my_list[i]).split(';')
                                    codigo_new,value = codigo.split('[')
                                    value_coma,wcoma = value.split("'")
                                    pais_new = pais.split("]")
                                    try:
                                        codigo_int = int(wcoma)
                                    except ValueError:
                                        files_failed.append(str(afile))
                                        break
                                    try:
                                        descripcion_str = str(pais_new[0])
                                    except ValueError:
                                        files_failed.append(str(afile))
                                        break
                            elif choices == '7':
                                for i in range(1,len(my_list)):
                                    nandina,cpc,cuode,cgce,sistema_armotizado,ciiu3,cuci3 = str(my_list[i]).split(';')
                                    codigo_new,value = nandina.split('[')
                                    value_coma,wcoma = value.split("'")
                                    cuci3_new = cuci3.split("]")
                                    try:
                                        nandina_int = int(wcoma)
                                    except ValueError:
                                        files_failed.append(str(afile))
                                        error_find.append(wcoma)
                                        break
                                    try:
                                        cpc_int = int(cpc)
                                    except ValueError:
                                        files_failed.append(str(afile))
                                        error_find.append(cpc)
                                        break
                                    try:
                                        cuode_int = int(cuode)
                                    except ValueError:
                                        files_failed.append(str(afile))
                                        error_find.append(cuode)
                                        break
                                    try:
                                        cgce_int = int(cgce)
                                    except ValueError:
                                        files_failed.append(str(afile))
                                        error_find.append(cgce)
                                        break
                                    try:
                                        sistema_armotizado_int = int(sistema_armotizado)
                                    except ValueError:
                                        files_failed.append(str(afile))
                                        error_find.append(sistema_armotizado)
                                        break
                                    try:
                                        ciiu3_int = int(ciiu3)
                                    except ValueError:
                                        files_failed.append(str(afile))
                                        error_find.append(ciiu3)
                                        break
                                    try:
                                        descripcion_str = str(cuci3_new[0])
                                    except ValueError:
                                        files_failed.append(str(afile))
                                        error_find.append(cuci3_new[0])
                                        break
                            elif choices == '8':
                                for i in range(1,len(my_list)):
                                    ano,mes,pais,subpartida_nandina,peso,fob = str(my_list[i]).split(';')
                                    ano_new,value = ano.split('[')
                                    value_coma,wcoma = value.split("'")
                                    fob_new = fob.split("]")
                                    val1,val2 = fob_new[0].split("'")
                                    try:
                                        ano_int = int(wcoma)
                                    except ValueError:
                                        files_failed.append(str(afile))
                                        error_find.append('wcoma')
                                        break
                                    try:
                                        mes_int = int(mes)
                                    except ValueError:
                                        files_failed.append(str(afile))
                                        error_find.append('mes')
                                        break
                                    try:
                                        pais_int = int(pais)
                                    except ValueError:
                                        files_failed.append(str(afile))
                                        error_find.append('pais')
                                        break
                                    try:
                                        subpartida_nandina_int = int(subpartida_nandina)
                                    except ValueError:
                                        files_failed.append(str(afile))
                                        error_find.append('subpartida_nandina')
                                        break
                                    try:
                                        peso_float = str(peso)
                                    except ValueError:
                                        files_failed.append(str(afile))
                                        error_find.append('peso')
                                        break
                                    try:
                                        fob_float = str(val2)
                                    except ValueError:
                                        files_failed.append(str(afile))
                                        error_find.append('val2')
                                        break
                            else:
                                for i in range(1,len(my_list)):
                                    ano,mes,pais,subpartida_nandina,peso,fob,cif = str(my_list[i]).split(';')
                                    ano_new,value = ano.split('[')
                                    value_coma,wcoma = value.split("'")
                                    cif_new = cif.split("]")
                                    val1,val2 = cif_new[0].split("'")
                                    try:
                                        ano_int = int(wcoma)
                                    except ValueError:
                                        files_failed.append(str(afile))
                                        error_find.append('wcoma')
                                        break
                                    try:
                                        mes_int = int(mes)
                                    except ValueError:
                                        files_failed.append(str(afile))
                                        error_find.append('mes')
                                        break
                                    try:
                                        pais_int = int(pais)
                                    except ValueError:
                                        files_failed.append(str(afile))
                                        error_find.append('pais')
                                        break
                                    try:
                                        subpartida_nandina_int = int(subpartida_nandina)
                                    except ValueError:
                                        files_failed.append(str(afile))
                                        error_find.append('subpartida_nandina')
                                        break
                                    try:
                                        peso_float = str(peso)
                                    except ValueError:
                                        files_failed.append(str(afile))
                                        error_find.append('peso')
                                        break
                                    try:
                                        fob_float = str(fob)
                                    except ValueError:
                                        files_failed.append(str(afile))
                                        error_find.append('fob')
                                        break
                                    try:
                                        descripcion_str = str(val2)
                                    except ValueError:
                                        files_failed.append(str(afile))
                                        error_find.append('cif')
                                        break
                    
                    # Borramos los archivos que tienen mal formato.
                    print error_find
                    if len(files_failed) > 0:
                        for afile in files_failed:
                            os.remove(path_dir+str(afile))
                    if len(files_failed) == len(file_list):
                        return HttpResponseRedirect('/error/')
                    else:
                        #Luego se corre el load_files.sh
                        p = subprocess.Popen(['/home/ciec/oese/load_files_comercio',dbtable])
                        alert = p.communicate()
                        upload_success = True
                        empty = False

                        if choices == '8':
                            cursor = connection.cursor()
                            # Se realiza un update para ingresar datos a la columna subpartida_nandina_key
                            cursor.execute("UPDATE comercio_export_nandina SET subpartida_key=substr(subpartida_nandina,1,8)")
                            cursor.close
                            actualizar = True
                        elif choices == '9':
                            cursor = connection.cursor()
                            # Se realiza un update para ingresar datos a la columna subpartida_nandina_key
                            cursor.execute("UPDATE comercio_import_nandina SET subpartida_key=substr(subpartida_nandina,1,8)")
                            cursor.close
                            actualizar = True
            else:
                empty = True
                upload_success = False
        else:
            upload_form = UploadFileForm()
            upload_success = False
    else:
        return HttpResponseRedirect('/acceso_denegado/')

    return render_to_response(template, {'files_failed': files_failed,'upload_form': upload_form, 'upload_success':upload_success, 'empty':empty, 'actualizar':actualizar}, context)

def access_denied(request):
    template = 'access_denied.html'
    return render_to_response(template, context_instance=RequestContext(request, locals()))

def error_subida(request):
    template = 'error.html'
    return render_to_response(template, context_instance=RequestContext(request, locals()))

def actualizar_datos(request):
    template = 'update.html'
    return render_to_response(template, context_instance=RequestContext(request, locals()))

def option(request):
    data_result = []
    valor_k = request.GET['valor_k']
    tabla_export = ['comercio_export_cgce','comercio_export_ciiu3','comercio_export_cpc','comercio_export_cuode']
    tabla_import = ['comercio_import_cgce','comercio_import_ciiu3','comercio_import_cpc','comercio_import_cuode']

    if valor_k == '0':
        for i in xrange(0, len(tabla_export)):
            raw_delete = ("""TRUNCATE TABLE %s""") %(tabla_export[i])
            cursor = connection.cursor()
            cursor.execute(raw_delete)
            cursor.close
        result = equivalencia(0)
    else:
        for i in xrange(0, len(tabla_import)):
            raw_delete = ("""TRUNCATE TABLE %s""") %(tabla_import[i])
            cursor = connection.cursor()
            cursor.execute(raw_delete)
            cursor.close
        result = equivalencia(1)

    data_result.append([result])
    message = json.dumps(data_result, cls=PythonObjectEncoder)
    return HttpResponse(message, content_type='application/json')

def eliminar_datos_comercio(request):
    template = 'delete_comercio.html'
    data_paises = Paises.objects.all()
    return render_to_response(template, context_instance=RequestContext(request, locals()))

def eliminar_comercio(request):
    txt_code = request.GET['txt_code']
    txt_choice = request.GET['txt_choice']
    permiso = True

    if txt_code == "":
        flag = [0]
    else:
        try:
            txt_code_int = int(txt_code)
        except ValueError:
            permiso = False
            flag = [1]
        
        if permiso:
            txt_code_int = int(txt_code)
            txt_choice_int = int(txt_choice)

            if txt_choice_int == 1:
                db_comercio = Export_NANDINA
            else:
                db_comercio = Import_NANDINA

            buscar_existe_pais = db_comercio.objects.filter(pais=txt_code_int)

            if buscar_existe_pais.count() > 0:
                buscar_existe_pais.delete()
                flag = [3]
            else:
                flag = [2]

    message = json.dumps(flag, cls=PythonObjectEncoder)
    return HttpResponse(message, content_type='application/json')

def ajax_name_standars(request):
    standar_value = request.GET['standar_value']

    if standar_value == '1':
        str_val = 'NANDINA'
    elif standar_value == '2':
        str_val = 'CGCE'
    elif standar_value == '3':
        str_val = 'CIIU3'
    elif standar_value == '4':
        str_val = 'CPC'

    message = json.dumps(str_val, cls=PythonObjectEncoder)
    return HttpResponse(message, content_type='application/json')

def ajax_level_standars(request):
    standar_level = request.GET['standar_level']
    values_permitted = []

    if standar_level == '1':
        values_permitted = [2,4,6,8,10]
    elif standar_level == '2':
        values_permitted = [1,2,3]
    elif standar_level == '3':
        values_permitted = [2,3,4]
    elif standar_level == '4':
        values_permitted = [1,2,3,4,5]

    message = json.dumps(values_permitted, cls=PythonObjectEncoder)
    return HttpResponse(message, content_type='application/json')

def show_code_standars(request):
    template = 'show_code_standars.html'
    return render_to_response(template, context_instance=RequestContext(request, locals()))

def filter_code_standars(request):
    standar_value = request.GET['standar_value']
    standar_result = []

    if standar_value == '1':
        db_name = NANDINA
    elif standar_value == '2':
        db_name = CGCE
    elif standar_value == '3':
        db_name = CIIU3
    elif standar_value == '4':
        db_name = CPC
    else:
        db_name = CUODE

    object_standar = db_name.objects.all()
    
    for standars in object_standar:
        dict_standars = {}
        if standar_value == '1':
            dict_standars['codigo'] = standars.subpartida
        else:
            dict_standars['codigo'] = standars.codigo
        dict_standars['descripcion'] = standars.descripcion
        standar_result.append(dict_standars)

    message = json.dumps(standar_result, cls=PythonObjectEncoder)
    return HttpResponse(message, content_type='application/json')

def export_import_total(request):
    cursor = connection.cursor()
    period = request.GET['period']
    txt_desde = request.GET['txt_desde'].encode('ascii','ignore').replace('/', '-')+'-01'
    txt_hasta = request.GET['txt_hasta'].encode('ascii','ignore').replace('/', '-')+'-01'
    tipo = request.GET['tipo']
    bandera = 0
    data_result = []

    if tipo == '1':
        db_table = 'comercio_export_total'
        bandera = 0
    else:
        db_table = 'comercio_import_total'
        bandera = 1

    if period == '4':
        ini_date = txt_desde[0:4]
        fin_date = txt_hasta[0:4]
    else:
        ini_date = str(txt_desde)
        fin_date = str(txt_hasta)

    if bandera == 0:
        if period == '1':
            raw_body = ('''  SELECT id, ano as ANO, substr(ifnull(date(concat(ANO,'-0',MES,'-01')),date(concat(ANO,'-',MES,'-01'))),1,7) AS FECHA, SUM(fob) AS FOB, SUM(peso) AS PESO FROM  %s GROUP BY ANO, FECHA HAVING (FECHA>='%s') AND (FECHA<='%s') ''') %(db_table, ini_date, fin_date)
        elif period == '2':
            raw_body  = (''' SELECT id, ano as ANO, CONCAT(ANO,'-0',FLOOR(((MES-1)/3)+1)) AS FECHA, SUM(fob) AS FOB, SUM(peso) AS PESO FROM  %s GROUP BY ANO, FECHA HAVING (FECHA>='%s') AND (FECHA<='%s') ''') %(db_table, ini_date, fin_date)
        elif period == '3':
            raw_body  = (''' SELECT id, ano as ANO, CONCAT(ANO,'-0',FLOOR(((MES-1)/6)+1)) AS FECHA, SUM(fob) AS FOB, SUM(peso) AS PESO FROM  %s GROUP BY ANO, FECHA HAVING (FECHA>='%s') AND (FECHA<='%s') ''') %(db_table, ini_date, fin_date)
        else:
            raw_body  = (''' SELECT id, ano as ANO, SUM(fob) AS FOB, SUM(peso) AS PESO FROM %s GROUP BY ANO HAVING (ANO>=%s) AND (ANO<=%s) ''') %(db_table, ini_date, fin_date)
    else:
        if period == '1':
            raw_body = ('''  SELECT id, ano as ANO, substr(ifnull(date(concat(ANO,'-0',MES,'-01')),date(concat(ANO,'-',MES,'-01'))),1,7) AS FECHA, SUM(fob) AS FOB, SUM(peso) AS PESO, SUM(cif) AS CIF FROM  %s GROUP BY ANO, FECHA HAVING (FECHA>='%s') AND (FECHA<='%s') ''') %(db_table, ini_date, fin_date)
        elif period == '2':
            raw_body  = (''' SELECT id, ano as ANO, CONCAT(ANO,'-0',FLOOR(((MES-1)/3)+1)) AS FECHA, SUM(fob) AS FOB, SUM(peso) AS PESO, SUM(cif) AS CIF FROM  %s GROUP BY ANO, FECHA HAVING (FECHA>='%s') AND (FECHA<='%s') ''') %(db_table, ini_date, fin_date)
        elif period == '3':
            raw_body  = (''' SELECT id, ano as ANO, CONCAT(ANO,'-0',FLOOR(((MES-1)/6)+1)) AS FECHA, SUM(fob) AS FOB, SUM(peso) AS PESO, SUM(cif) AS CIF FROM  %s GROUP BY ANO, FECHA HAVING (FECHA>='%s') AND (FECHA<='%s') ''') %(db_table, ini_date, fin_date)
        else:
            raw_body  = (''' SELECT id, ano as ANO, SUM(fob) AS FOB, SUM(peso) AS PESO, SUM(cif) AS CIF FROM %s GROUP BY ANO HAVING (ANO>=%s) AND (ANO<=%s) ''') %(db_table, ini_date, fin_date)
        
    cursor.execute(raw_body)
    table_result = cursor.fetchall()
    
    # Validar por año
    for data in table_result:
        if bandera == 0:
            if period == '4':
                data_result.append([data[1], float(data[2]), float(data[3])])
            else:
                data_result.append([data[1], data[2], float(data[3]), float(data[4])])
        else:
            if period == '4':
                data_result.append([data[1], float(data[2]), float(data[3]), float(data[4])])
            else:
                data_result.append([data[1], data[2], float(data[3]), float(data[4]), float(data[5])])

    message = json.dumps(data_result, cls=PythonObjectEncoder)
    return HttpResponse(message, content_type='application/json')