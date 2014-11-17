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
# import csv
# import os
# import subprocess
# import xlrd
# from os import listdir
# from os.path import isfile, join
# from django.db import connection

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
        standar_name = NANDINA
        standar_table = 'comercio_nandina'
        export_standar_name = Export_NANDINA
        export_standar_table = 'comercio_export_nandina'
        import_standar_name = Import_NANDINA
        import_standar_table = 'comercio_import_nandina'
    else:
        standar_clase = standar_var1 = standar_var2 = 'codigo'
        if standar == '2':
            standar_name = CGCE
            standar_table = 'comercio_cgce'
            export_standar_name = Export_CGCE
            export_standar_table = 'comercio_export_cgce'
            import_standar_name = Import_CGCE
            import_standar_table = 'comercio_import_cgce'
        elif standar == '3':
            standar_name = CIIU3
            standar_table = 'comercio_ciiu3'
            export_standar_name = Export_CIIU3
            export_standar_table = 'comercio_export_ciiu3'
            import_standar_name = Import_CIIU3
            import_standar_table = 'comercio_import_ciiu3'
        elif standar == '4':
            standar_name = CPC
            standar_table = 'comercio_cpc'
            export_standar_name = Export_CPC
            export_standar_table = 'comercio_export_cpc'
            import_standar_name = Import_CPC
            import_standar_table = 'comercio_import_cpc'
        elif standar == '5':
            standar_name = CUODE
            standar_table = 'comercio_cuode'
            export_standar_name = Export_CUODE
            export_standar_table = 'comercio_export_cuode'
            import_standar_name = Import_CUODE
            import_standar_table = 'comercio_import_cuode'

    table_A = sql_A(standar_name, standar_table, standar_clase, value_A, value_B)

    if standar == '1':
        for va in table_A:
            data_table_A.append([va.subpartida, va.descripcion])
    else:
        for va in table_A:
            data_table_A.append([va.codigo, va.descripcion])

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
        tipo_standar_name = export_standar_name
        tipo_standar_table = export_standar_table
    else:
        tipo_standar_name = import_standar_name
        tipo_standar_table = import_standar_table

    if option == '1':
        table_B = sql_B_clase(tipo, tipo_standar_name, tipo_standar_table, standar_table, standar_clase,
                                        standar_var1, standar_var2, period, value_A, value_B, agreg, ini_date, fin_date, checkbox_pais)

    else:
        table_B = sql_B_pais(tipo, tipo_standar_name, tipo_standar_table, standar_name, standar_table, standar_clase,
                                        standar_var1, standar_var2, period, value, agreg, ini_date, fin_date)


    totalPeso = 0
    totalFOB = 0
    totalCIF = 0

    if checkbox_pais == '0':
        if tipo == '1':
            if period == '4':
                if standar == '1':
                    for vb in table_B:
                        totalPeso = totalPeso + float(vb.PESO)
                        totalFOB = totalFOB + float(vb.SUBTOTAL_FOB)
                        data_table_B.append([vb.ANO, vb.subpartida, float(vb.PESO), float(vb.SUBTOTAL_FOB)])
                else:
                    for vb in table_B:
                        totalPeso = totalPeso + float(vb.PESO)
                        totalFOB = totalFOB + float(vb.SUBTOTAL_FOB)
                        data_table_B.append([vb.ANO, vb.codigo, float(vb.PESO), float(vb.SUBTOTAL_FOB)])
            else:
                if standar == '1':
                    for vb in table_B:
                        totalPeso = totalPeso + float(vb.PESO)
                        totalFOB = totalFOB + float(vb.SUBTOTAL_FOB)
                        data_table_B.append([vb.FECHA, vb.subpartida, float(vb.PESO), float(vb.SUBTOTAL_FOB)])
                else:
                    for vb in table_B:
                        totalPeso = totalPeso + float(vb.PESO)
                        totalFOB = totalFOB + float(vb.SUBTOTAL_FOB)
                        data_table_B.append([vb.FECHA, vb.codigo, float(vb.PESO), float(vb.SUBTOTAL_FOB)])
        else:
            if period == '4':
                if standar == '1':
                    for vb in table_B:
                        totalPeso = totalPeso + float(vb.PESO)
                        totalFOB = totalFOB + float(vb.SUBTOTAL_FOB)
                        totalCIF = totalCIF + float(vb.SUBTOTAL_CIF)
                        data_table_B.append([vb.ANO, vb.subpartida, float(vb.PESO), float(vb.SUBTOTAL_FOB), float(vb.SUBTOTAL_CIF)])
                else:
                    for vb in table_B:
                        totalPeso = totalPeso + float(vb.PESO)
                        totalFOB = totalFOB + float(vb.SUBTOTAL_FOB)
                        totalCIF = totalCIF + float(vb.SUBTOTAL_CIF)
                        data_table_B.append([vb.ANO, vb.codigo, float(vb.PESO), float(vb.SUBTOTAL_FOB), float(vb.SUBTOTAL_CIF)])
            else:
                if standar == '1':
                    for vb in table_B:
                        totalPeso = totalPeso + float(vb.PESO)
                        totalFOB = totalFOB + float(vb.SUBTOTAL_FOB)
                        totalCIF = totalCIF + float(vb.SUBTOTAL_CIF)
                        data_table_B.append([vb.FECHA, vb.subpartida, float(vb.PESO), float(vb.SUBTOTAL_FOB), float(vb.SUBTOTAL_CIF)])
                else:
                    for vb in table_B:
                        totalPeso = totalPeso + float(vb.PESO)
                        totalFOB = totalFOB + float(vb.SUBTOTAL_FOB)
                        totalCIF = totalCIF + float(vb.SUBTOTAL_CIF)
                        data_table_B.append([vb.FECHA, vb.codigo, float(vb.PESO), float(vb.SUBTOTAL_FOB), float(vb.SUBTOTAL_CIF)])

    if checkbox_pais == '1' or option == '2':
        if tipo == '1':
            if period == '4':
                if standar == '1':
                    for vb in table_B:
                        totalPeso = totalPeso + float(vb.PESO)
                        totalFOB = totalFOB + float(vb.SUBTOTAL_FOB)
                        data_table_B.append([vb.ANO, vb.PAIS, vb.subpartida, float(vb.PESO), float(vb.SUBTOTAL_FOB)])
                else:
                    for vb in table_B:
                        totalPeso = totalPeso + float(vb.PESO)
                        totalFOB = totalFOB + float(vb.SUBTOTAL_FOB)
                        data_table_B.append([vb.ANO, vb.PAIS, vb.codigo, float(vb.PESO), float(vb.SUBTOTAL_FOB)])
            else:
                if standar == '1':
                    for vb in table_B:
                        totalPeso = totalPeso + float(vb.PESO)
                        totalFOB = totalFOB + float(vb.SUBTOTAL_FOB)
                        data_table_B.append([vb.FECHA, vb.PAIS, vb.subpartida, float(vb.PESO), float(vb.SUBTOTAL_FOB)])
                else:
                    for vb in table_B:
                        totalPeso = totalPeso + float(vb.PESO)
                        totalFOB = totalFOB + float(vb.SUBTOTAL_FOB)
                        data_table_B.append([vb.FECHA, vb.PAIS, vb.codigo, float(vb.PESO), float(vb.SUBTOTAL_FOB)])
        else:
            if period == '4':
                if standar == '1':
                    for vb in table_B:
                        totalPeso = totalPeso + float(vb.PESO)
                        totalFOB = totalFOB + float(vb.SUBTOTAL_FOB)
                        totalCIF = totalCIF + float(vb.SUBTOTAL_CIF)
                        data_table_B.append([vb.ANO, vb.PAIS, vb.subpartida, float(vb.PESO), float(vb.SUBTOTAL_FOB), float(vb.SUBTOTAL_CIF)])
                else:
                    for vb in table_B:
                        totalPeso = totalPeso + float(vb.PESO)
                        totalFOB = totalFOB + float(vb.SUBTOTAL_FOB)
                        totalCIF = totalCIF + float(vb.SUBTOTAL_CIF)
                        data_table_B.append([vb.ANO, vb.PAIS, vb.codigo, float(vb.PESO), float(vb.SUBTOTAL_FOB), float(vb.SUBTOTAL_CIF)])
            else:
                if standar == '1':
                    for vb in table_B:
                        totalPeso = totalPeso + float(vb.PESO)
                        totalFOB = totalFOB + float(vb.SUBTOTAL_FOB)
                        totalCIF = totalCIF + float(vb.SUBTOTAL_CIF)
                        data_table_B.append([vb.FECHA, vb.PAIS, vb.subpartida, float(vb.PESO), float(vb.SUBTOTAL_FOB), float(vb.SUBTOTAL_CIF)])
                else:
                    for vb in table_B:
                        totalPeso = totalPeso + float(vb.PESO)
                        totalFOB = totalFOB + float(vb.SUBTOTAL_FOB)
                        totalCIF = totalCIF + float(vb.SUBTOTAL_CIF)
                        data_table_B.append([vb.FECHA, vb.PAIS, vb.codigo, float(vb.PESO), float(vb.SUBTOTAL_FOB), float(vb.SUBTOTAL_CIF)])

    data_result.append([data_table_B])

    if(tipo == 1):
        data_result.append([totalPeso, totalFOB])
    else:
        data_result.append([totalPeso, totalFOB, totalCIF])

    message = json.dumps(data_result, cls=PythonObjectEncoder)
    return HttpResponse(message, content_type='application/json')


#standar_name: NANDINA, CGCE, CPC, CUODE, CIIU3 (objetos)
#standar_table: comercio_nandina, comercio_cgce, comercio_cpc, comercio_cuode, comercio_ciiu3 (nombre propio de la base)
#standar_clase: subpartida o codigo
#value_A: patron% o null segun 'BuscarPor'
#value_B: patron% o null segun 'BuscarPor'
def sql_A(standar_name, standar_table, standar_clase, value_A, value_B):
    raw_body = ("SELECT * FROM %s WHERE %s ") % (standar_table, standar_clase)
    raw_where = ("LIKE %s OR descripcion LIKE %s")
    table_A = standar_name.objects.raw(raw_body+raw_where, [value_A, value_B])
    return table_A


#tipo: tab_selected
#standar_name: NANDINA, CGCE, CPC, CUODE, CIIU3 (objetos)
#standar_table: comercio_nandina, comercio_cgce, comercio_cpc, comercio_cuode, comercio_ciiu3 (nombre propio de la base)
#standar_clase: subpartida o codigo
#periodicidad: mes, trimestre, semestre, anual
#value_A: patron% o null segun 'BuscarPor'
#value_B: patron% o null segun 'BuscarPor'
#agreg: # nivel de agregacion
#ini_date: desde.substring(0,4)
#fin_date: hasta.substring(0,4)
#checkbox_pais: si se separa por pais o no
def sql_B_clase(tipo, tipo_standar_name, tipo_standar_table, standar_table, standar_clase,
                        standar_var1, standar_var2, period, value_A, value_B, agreg, ini_date, fin_date, checkbox_pais):

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

        table_B = tipo_standar_name.objects.raw(raw_body_1 + raw_body_2 + raw_where_1 + raw_body_3 + raw_where_2, [value_A, value_B,  ini_date, fin_date])

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

            table_B = tipo_standar_name.objects.raw(raw_body_1 + raw_body_2 + raw_where_1 + raw_body_3 + raw_where_2, [value_A, value_B,  ini_date, fin_date])

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

            table_B = tipo_standar_name.objects.raw(raw_body_1 + raw_body_2 + raw_where_1 + raw_body_3 + raw_where_2, [value_A, value_B, ini_date, fin_date])

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

            table_B = tipo_standar_name.objects.raw(raw_body_1 + raw_body_2 + raw_where_1 + raw_body_3 + raw_where_2, [value_A, value_B,  ini_date, fin_date])

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

            table_B = tipo_standar_name.objects.raw(raw_body_1 + raw_body_2 + raw_where_1 + raw_body_3 + raw_where_2, [value_A, value_B, ini_date, fin_date])

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

            table_B = tipo_standar_name.objects.raw(raw_body_1 + raw_body_2 + raw_where_1 + raw_body_3 + raw_where_2, [value_A, value_B,  ini_date, fin_date])

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

            table_B = tipo_standar_name.objects.raw(raw_body_1 + raw_body_2 + raw_where_1 + raw_body_3 + raw_where_2, [value_A, value_B, ini_date, fin_date])

    return table_B


def sql_B_pais(tipo, tipo_standar_name, tipo_standar_table, standar_name, standar_table, standar_clase,
                      standar_var1, standar_var2, period, value, agreg, ini_date, fin_date):

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

        table_B = tipo_standar_name.objects.raw(raw_body_1 + raw_body_2 + raw_where_1 + raw_body_3 + raw_where_2, [value, ini_date, fin_date])

    #pais por trimestre
    elif period == '2':
        if tipo == '1':
            raw_body_1 = ("""SELECT id, concat(ANO,'-0',FLOOR(SEMESTRE)) AS FECHA,
                                    V_TABLE.pais AS PAIS,
                                    V_TABLE.PESO AS PESO,
                                    V_TABLE.SUBTOTAL_FOB AS SUBTOTAL_FOB
                                    FROM( SELECT comercio_paises.id, ano AS ANO, ((MES-1)/3)+1 AS SEMESTRE,
                                    comercio_paises.pais AS PAIS,
                                    substr(%s.%s,1,%s) AS %s,
                                    sum(peso) AS PESO,
                                    sum(fob) AS SUBTOTAL_FOB
                                   """) % (tipo_standar_table, standar_var1, agreg, standar_clase)
        else:
            raw_body_1 = ("""SELECT id, concat(ANO,'-0',FLOOR(SEMESTRE)) AS FECHA,
                                    V_TABLE.pais AS PAIS,
                                    V_TABLE.PESO AS PESO,
                                    V_TABLE.SUBTOTAL_FOB AS SUBTOTAL_FOB,
                                    V_TABLE.SUBTOTAL_CIF AS SUBTOTAL_CIF
                                    FROM( SELECT comercio_paises.id, ano AS ANO, ((MES-1)/3)+1 AS SEMESTRE,
                                    comercio_paises.pais AS PAIS,
                                    substr(%s.%s,1,%s) AS %s,
                                    sum(peso) AS PESO,
                                    sum(fob) AS SUBTOTAL_FOB,
                                    sum(cif) AS SUBTOTAL_CIF

                                   """) % (tipo_standar_table, standar_var1, agreg, standar_clase)

        raw_body_2 = ("""FROM %s
                                INNER JOIN comercio_paises ON %s.pais=comercio_paises.codigo
                                WHERE (%s.pais IN
                                (SELECT codigo FROM comercio_paises WHERE (pais
                                """) % (tipo_standar_table, tipo_standar_table, tipo_standar_table)

        raw_where_1 = ("LIKE %s))) ")

        raw_body_3 = ("GROUP BY ANO, SEMESTRE,substr(%s.%s,1,%s),%s.pais) AS V_TABLE ") % (tipo_standar_table, standar_var1, agreg, tipo_standar_table)

        raw_where_2 = ("WHERE (concat(ANO,'-0',FLOOR(SEMESTRE))>=%s) AND (concat(ANO,'-0',FLOOR(SEMESTRE))<=%s)")

        table_B = tipo_standar_name.objects.raw(raw_body_1 + raw_body_2 + raw_where_1 + raw_body_3 + raw_where_2, [value, ini_date, fin_date])

    #pais por semestre
    elif period == '3':
        if tipo == '1':
            raw_body_1 = ("""SELECT id, concat(ANO,'-0',FLOOR(SEMESTRE)) AS FECHA,
                                    V_TABLE.pais AS PAIS,
                                    V_TABLE.PESO AS PESO,
                                    V_TABLE.SUBTOTAL_FOB AS SUBTOTAL_FOB
                                    FROM( SELECT comercio_paises.id, ano AS ANO, ((MES-1)/6)+1 AS SEMESTRE,
                                    comercio_paises.pais AS PAIS,
                                    substr(%s.%s,1,%s) AS %s,
                                    sum(peso) AS PESO,
                                    sum(fob) AS SUBTOTAL_FOB
                                   """) % (tipo_standar_table, standar_var1, agreg, standar_clase)
        else:
            raw_body_1 = ("""SELECT id, concat(ANO,'-0',FLOOR(SEMESTRE)) AS FECHA,
                                    V_TABLE.pais AS PAIS,
                                    V_TABLE.PESO AS PESO,
                                    V_TABLE.SUBTOTAL_FOB AS SUBTOTAL_FOB.
                                    V_TABLE.SUBTOTAL_CIF AS SUBTOTAL_CIF
                                    FROM( SELECT comercio_paises.id, ano AS ANO, ((MES-1)/6)+1 AS SEMESTRE,
                                    comercio_paises.pais AS PAIS,
                                    substr(%s.%s,1,%s) AS %s,
                                    sum(peso) AS PESO,
                                    sum(fob) AS SUBTOTAL_FOB,
                                    sum(cif) AS SUBTOTAL_CIF

                                   """) % (tipo_standar_table, standar_var1, agreg, standar_clase)

        raw_body_2 = ("""FROM %s
                                INNER JOIN comercio_paises ON %s.pais=comercio_paises.codigo
                                WHERE (%s.pais IN
                                (SELECT codigo FROM comercio_paises WHERE (pais
                                """) % (tipo_standar_table, tipo_standar_table, tipo_standar_table)

        raw_where_1 = ("LIKE %s))) ")

        raw_body_3 = ("GROUP BY ANO, SEMESTRE,substr(%s.%s,1,%s),%s.pais) AS V_TABLE ") % (tipo_standar_table, standar_var1, agreg, tipo_standar_table)

        raw_where_2 = ("WHERE (concat(ANO,'-0',FLOOR(SEMESTRE))>=%s) AND (concat(ANO,'-0',FLOOR(SEMESTRE))<=%s)")

        table_B = tipo_standar_name.objects.raw(raw_body_1 + raw_body_2 + raw_where_1 + raw_body_3 + raw_where_2, [value, ini_date, fin_date])

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

        table_B = tipo_standar_name.objects.raw(raw_body_1 + raw_body_2 + raw_where_1 + raw_body_3 + raw_where_2, [value, ini_date, fin_date])

    return table_B

def insert_data_comercio(request):
    context = RequestContext(request)
    template = 'insert_data_comercio.html'
    upload_success = False
    empty = False
    arreglo = []
    path_upload_csv = '/home/patu/Downloads/ObservatorioCIEC-master/media/csv/'
    user = request.user
    is_super_user = user.is_superuser

    try:
        if is_super_user:
            if request.method == 'POST':
                upload_form = UploadFileForm(request.POST, request.FILES)
                if 'file' in request.FILES:
                    if upload_form.is_valid():
                        file = upload_form.cleaned_data['file']
                        choices = upload_form.cleaned_data['choices']
                        # Subiendo el archivo seleccionado a la carpeta /media/csv/
                        new_file_import = upload_csv_file(upload=request.FILES['file'])
                        new_file_import.save()

                        # Una ves que se sube el archivo, se procede a leerlo
                        file_name = [ f for f in listdir(path_upload_csv) if isfile(join(path_upload_csv,f)) ]
                        workbook = xlrd.open_workbook(path_upload_csv+file_name[0])
                        worksheets = workbook.sheet_names()
                        for worksheet_name in worksheets:
                            current_worksheet = workbook.sheet_by_name(worksheet_name)
                            num_rows = current_worksheet.nrows -1
                            num_cells = current_worksheet.ncols - 1
                            curr_row = -1
                            while curr_row < num_rows:
                                curr_row +=1
                                row = current_worksheet.row(curr_row)
                                if curr_row == 0:
                                    pass
                                else:
                                    curr_cell = -1
                                    while curr_cell < num_cells:
                                        curr_cell += 1
                                        cell_type = current_worksheet.cell_type(curr_row, curr_cell)
                                        cell_value = current_worksheet.cell_value(curr_row, curr_cell)
                                        arreglo.append(cell_value)
                                        if (len(arreglo) == 2):
                                            new_codigo = str(arreglo[0])
                                            new_get_codigo = new_codigo.split('.',1)
                                            if choices == '1':
                                                new_data = CGCE(codigo=new_get_codigo[0],descripcion=arreglo[1])
                                                new_data.save()
                                                for x in arreglo[:]:
                                                    arreglo.remove(x)
                                            elif choices == '2':
                                                    new_data = CIIU3(codigo=new_get_codigo[0],descripcion=arreglo[1])
                                                    new_data.save()
                                                    for x in arreglo[:]:
                                                        arreglo.remove(x)
                                            elif choices =='3':
                                                    new_data = CPC(codigo=new_get_codigo[0],descripcion=arreglo[1])
                                                    new_data.save()
                                                    for x in arreglo[:]:
                                                        arreglo.remove(x)
                                            elif choices == '4':
                                                    new_data = CUODE(codigo=new_get_codigo[0],descripcion=arreglo[1])
                                                    new_data.save()
                                                    for x in arreglo[:]:
                                                        arreglo.remove(x)
                                            elif choices == '5':
                                                    new_data = NANDINA(subpartida=new_get_codigo[0],descripcion=arreglo[1])
                                                    new_data.save()
                                                    for x in arreglo[:]:
                                                        arreglo.remove(x)
                                            elif choices == '6':
                                                new_data = Paises(codigo=new_get_codigo[0],pais=arreglo[1])
                                                new_data.save()
                                                for x in arreglo[:]:
                                                    arreglo.remove(x)
                                        elif (len(arreglo) == 7):
                                            if choices == '7':
                                                new_data = Equivalencia(nandina=new_get_codigo[0],cpc=arreglo[1],cuode=arreglo[2],cgce=arreglo[3],sistema_armotizado=arreglo[4],ciiu3=arreglo[5],cuci3=arreglo[6])
                                                new_data.save()
                                                for x in arreglo[:]:
                                                    arreglo.remove(x)
                                        elif (len(arreglo) == 8):
                                            if choices == '8':
                                                get_subpartida_nandina = str(arreglo[3])
                                                new_subpartida_nandina = get_subpartida_nandina.split('.',1)
                                                try:
                                                    get_peso = arreglo[5]
                                                    new_peso = get_peso.split(',',1)
                                                    final_peso = new_peso[0]+new_peso[1]
                                                except Exception, e:
                                                    final_peso = arreglo[5]
                                                try:
                                                    get_fob = arreglo[6]
                                                    new_fob = get_fob.split(',',1)
                                                    final_fob = new_fob[0]+new_fob[1]                                                    
                                                except Exception, e:
                                                    final_fob = arreglo[6]
                                                new_data = Export_NANDINA(ano=arreglo[0],mes=arreglo[1],pais=arreglo[2],subpartida_nandina=new_subpartida_nandina[0],descripcion=arreglo[4],peso=final_peso,fob=final_fob,total_fob=arreglo[7])
                                                new_data.save()
                                                for x in arreglo[:]:
                                                    arreglo.remove(x)
                                        elif (len(arreglo) == 9):
                                            if choices == '9':
                                                get_subpartida_nandina = str(arreglo[3])
                                                new_subpartida_nandina = get_subpartida_nandina.split('.',1)
                                                try:
                                                    get_peso = arreglo[5]
                                                    new_peso = get_peso.split(',',1)
                                                    final_peso = new_peso[0]+new_peso[1]
                                                except Exception, e:
                                                    final_peso = arreglo[5]
                                                try:
                                                    get_fob = arreglo[6]
                                                    new_fob = get_fob.split(',',1)
                                                    final_fob = new_fob[0]+new_fob[1]   
                                                except Exception, e:
                                                    final_fob = arreglo[6]
                                                # Hace el insert de datos a la tabla comercio_import_nandina Import_NANDINA
                                                new_data = Import_NANDINA(ano=arreglo[0],mes=arreglo[1],pais=arreglo[2],subpartida_nandina=new_subpartida_nandina[0],descripcion=arreglo[4],peso=final_peso,fob=final_fob,cif=arreglo[7],total_fob=arreglo[8])
                                                new_data.save()
                                                for x in arreglo[:]:
                                                    arreglo.remove(x)
                        # Se hace un rm al archivo subido
                        os.remove(path_upload_csv+file_name[0])
                        if choices == '8':
                            # Se realiza un update a la columna subpartida_nandina si es que el lenght es igual a 9
                            cursor = connection.cursor()
                            cursor.execute("UPDATE comercio_export_nandina SET subpartida_nandina=concat('0',subpartida_nandina) WHERE LENGTH(subpartida_nandina)=9")
                            # Se realiza un update para ingresar datos a la columna subpartida_nandina_key
                            cursor.execute("UPDATE comercio_export_nandina SET subpartida_key=substr(subpartida_nandina,1,8)")
                        elif choices == '9':
                            cursor = connection.cursor()
                            cursor.execute("UPDATE comercio_import_nandina SET subpartida_nandina=concat('0',subpartida_nandina) WHERE LENGTH(subpartida_nandina)=9")
                            # Se realiza un update para ingresar datos a la columna subpartida_nandina_key
                            cursor.execute("UPDATE comercio_import_nandina SET subpartida_key=substr(subpartida_nandina,1,8)")
                    upload_success = True
                    empty = False
                else:
                    empty = True
                    upload_success = False
            else:
                upload_form = UploadFileForm()
                upload_success = False
        else:
            os.remove(path_upload_csv+file_name[0])
            return HttpResponseRedirect('/acceso_denegado/')
    except Exception, e:
        os.remove(path_upload_csv+file_name[0])
        return HttpResponseRedirect('/error-subida/')
    return render_to_response(template, {'upload_form': upload_form, 'upload_success':upload_success, 'empty':empty}, context)

def access_denied(request):
    template = 'access_denied.html'
    return render_to_response(template, context_instance=RequestContext(request, locals()))

def error_subida(request):
    template = 'error.html'
    return render_to_response(template, context_instance=RequestContext(request, locals()))
