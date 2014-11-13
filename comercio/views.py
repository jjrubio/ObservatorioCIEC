from django.shortcuts import HttpResponse, HttpResponseRedirect, render_to_response
from django.template.context import RequestContext
from django.template.loader import get_template
from models import *
import json
from django.core import serializers
from json import JSONEncoder
import pickle
from django.db.models import Q


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

    # tipo = '1'
    # option = '1'
    # search_by = '1'
    # standar = '5'
    # txt_desde = '2000/01'
    # txt_hasta = '2001/01'
    # period = '1'
    # txt_agregacion = '4'
    # txt_patron = ''
    # checkbox_pais = '0'

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

    if checkbox_pais == '0':
        if tipo == '1':
            if period == '4':
                if standar == '1':
                    for vb in table_B:
                        data_table_B.append([vb.ANO, vb.subpartida, float(vb.PESO), float(vb.SUBTOTAL_FOB)])
                else:
                    for vb in table_B:
                        data_table_B.append([vb.ANO, vb.codigo, float(vb.PESO), float(vb.SUBTOTAL_FOB)])
            else:
                if standar == '1':
                    for vb in table_B:
                        data_table_B.append([vb.FECHA, vb.subpartida, float(vb.PESO), float(vb.SUBTOTAL_FOB)])
                else:
                    for vb in table_B:
                        data_table_B.append([vb.FECHA, vb.codigo, float(vb.PESO), float(vb.SUBTOTAL_FOB)])
        else:
            if period == '4':
                if standar == '1':
                    for vb in table_B:
                        data_table_B.append([vb.ANO, vb.subpartida, float(vb.PESO), float(vb.SUBTOTAL_FOB), float(vb.SUBTOTAL_CIF)])
                else:
                    for vb in table_B:
                        data_table_B.append([vb.ANO, vb.codigo, float(vb.PESO), float(vb.SUBTOTAL_FOB), float(vb.SUBTOTAL_CIF)])
            else:
                if standar == '1':
                    for vb in table_B:
                        data_table_B.append([vb.FECHA, vb.subpartida, float(vb.PESO), float(vb.SUBTOTAL_FOB), float(vb.SUBTOTAL_CIF)])
                else:
                    for vb in table_B:
                        data_table_B.append([vb.FECHA, vb.codigo, float(vb.PESO), float(vb.SUBTOTAL_FOB), float(vb.SUBTOTAL_CIF)])

    if checkbox_pais == '1' or option == '2':
        if tipo == '1':
            if period == '4':
                if standar == '1':
                    for vb in table_B:
                        data_table_B.append([vb.ANO, vb.PAIS, vb.subpartida, float(vb.PESO), float(vb.SUBTOTAL_FOB)])
                else:
                    for vb in table_B:
                        data_table_B.append([vb.ANO, vb.PAIS, vb.codigo, float(vb.PESO), float(vb.SUBTOTAL_FOB)])
            else:
                if standar == '1':
                    for vb in table_B:
                        data_table_B.append([vb.FECHA, vb.PAIS, vb.subpartida, float(vb.PESO), float(vb.SUBTOTAL_FOB)])
                else:
                    for vb in table_B:
                        data_table_B.append([vb.FECHA, vb.PAIS, vb.codigo, float(vb.PESO), float(vb.SUBTOTAL_FOB)])
        else:
            if period == '4':
                if standar == '1':
                    for vb in table_B:
                        data_table_B.append([vb.ANO, vb.PAIS, vb.subpartida, float(vb.PESO), float(vb.SUBTOTAL_FOB), float(vb.SUBTOTAL_CIF)])
                else:
                    for vb in table_B:
                        data_table_B.append([vb.ANO, vb.PAIS, vb.codigo, float(vb.PESO), float(vb.SUBTOTAL_FOB), float(vb.SUBTOTAL_CIF)])
            else:
                if standar == '1':
                    for vb in table_B:
                        data_table_B.append([vb.FECHA, vb.PAIS, vb.subpartida, float(vb.PESO), float(vb.SUBTOTAL_FOB), float(vb.SUBTOTAL_CIF)])
                else:
                    for vb in table_B:
                        data_table_B.append([vb.FECHA, vb.PAIS, vb.codigo, float(vb.PESO), float(vb.SUBTOTAL_FOB), float(vb.SUBTOTAL_CIF)])

    data_result.append([data_table_B])

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

            raw_where = ("LIKE %s) OR (descripcion LIKE %s))) GROUP BY ANO, SEMESTRE) AS V_TABLE WHERE (concat(ANO,'-0',FLOOR(SEMESTRE))>=%s) AND (concat(ANO,'-0',FLOOR(SEMESTRE))<=%s)")

            table_B = tipo_standar_name.objects.raw(raw_body_1 + raw_body_2 + raw_where, [value_A, value_B,  ini_date, fin_date])

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

            raw_where = ("LIKE %s) OR (descripcion LIKE %s))) GROUP BY ANO, SEMESTRE) AS V_TABLE WHERE (concat(ANO,'-0',FLOOR(SEMESTRE))>=%s) AND (concat(ANO,'-0',FLOOR(SEMESTRE))<=%s)")

            table_B = tipo_standar_name.objects.raw(raw_body_1 + raw_body_2 + raw_where, [value_A, value_B,  ini_date, fin_date])

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

            raw_where = ("LIKE %s) OR (descripcion LIKE %s))) GROUP BY ANO HAVING(ANO>=%s) AND (ANO<=%s)")

            table_B = tipo_standar_name.objects.raw(raw_body_1 + raw_body_2 + raw_where, [value_A, value_B,  ini_date, fin_date])

        else:
            if tipo == '1':
                raw_body_1 = ("""SELECT %s.id, ano AS ANO,
                                        comercio_paises.pais AS PAIS,
                                        substr(%s.%s,1,%s) AS %s,
                                        sum(peso) AS PESO,
                                        sum(fob) AS SUBTOTAL_FOB
                                       """) % (tipo_standar_table, tipo_standar_table, standar_var1, agreg, standar_clase)
            else:
                raw_body_1 = ("""SELECT id, ano AS ANO,
                                        comercio_paises.pais AS PAIS,
                                        substr(%s,1,%s) AS %s,
                                        sum(peso) AS PESO,
                                        sum(fob) AS SUBTOTAL_FOB,
                                        sum(cif) AS SUBTOTAL_CIF
                                       """) % (standar_var1, agreg, standar_clase)

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

        table_B = tipo_standar_name.objects.raw(raw_body_1 + raw_body_2 + raw_where_1 + raw_body_3 + raw_where_2, [value, ini_date, fin_date])

    #pais por semestre
    elif period == '3':
        if tipo == '1':
            raw_body_1 = ("""SELECT id, concat(ANO,'-0',FLOOR(SEMESTRE)) AS FECHA,
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

        table_B = tipo_standar_name.objects.raw(raw_body_1 + raw_body_2 + raw_where_1 + raw_body_3 + raw_where_2, [value, ini_date, fin_date])

    #pais por ano
    elif period == '4':
        if tipo == '1':
            raw_body_1 = ("""SELECT %s.id, ano AS ANO,
                                    comercio_paises.pais AS PAIS,
                                    substr(%s.%s,1,%s) AS %s,
                                    sum(peso) AS PESO,
                                    sum(fob) AS SUBTOTAL_FOB
                                   """) % (tipo_standar_table, tipo_standar_table, standar_var1, agreg, standar_clase)
        else:
            raw_body_1 = ("""SELECT id, ano AS ANO,
                                    comercio_paises.pais AS PAIS,
                                    substr(%s,1,%s) AS %s,
                                    sum(peso) AS PESO,
                                    sum(fob) AS SUBTOTAL_FOB,
                                    sum(cif) AS SUBTOTAL_CIF
                                   """) % (standar_var1, agreg, standar_clase)

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
    template = 'insert_data_comercio.html'
    return render_to_response(template, context_instance=RequestContext(request, locals()))