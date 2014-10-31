from django.shortcuts import HttpResponse, HttpResponseRedirect, render_to_response
from django.template.context import RequestContext
from django.template.loader import get_template
from models import *
import json
from django.core import serializers
from json import JSONEncoder
from django.db.models import Q

def comercio_page(request):
    template = 'comercio.html'
    return render_to_response(template, context_instance = RequestContext(request,locals()))


def comercio(request):
    tab_selected = request.GET['tab_selected']
    option = request.GET['option']
    search_by = request.GET['search_by']
    standar = request.GET['standar']
    txt_desde = request.GET['txt_desde']
    txt_hasta = request.GET['txt_hasta']
    period = request.GET['period']
    txt_agregacion = request.GET['txt_agregacion']
    txt_patron = request.GET['txt_patron']
    checkbox_select = request.GET['checkbox_select']

    if option == '1':
        if search_by == '1':
            value_A = txt_patron+'%'
            value_B = None
        else:
            value_A = None
            value_B = '%'+txt_patron+'%'
    else:
        pass

    if standar == '1':
        standar_codigo = 'subpartida'
        standar_name = NANDINA
        standar_table = 'comercio_nandina'
        export_standar_name = Export_NANDINA
        import_standar_table = 'comercio_export_nandina'
        import_standar_name = Import_NANDINA
        import_standar_table = 'comercio_import_nandina'
    else:
        standar_codigo = 'codigo'
        if standar == '2':
            standar_name = CGCE
            standar_table = 'comercio_cgce'
            export_standar_name = Export_CGCE
            import_standar_table = 'comercio_export_cgce'
            import_standar_name = Import_CGCE
            import_standar_table = 'comercio_import_cgce'
        elif standar == '3':
            standar_name = CIIU3
            standar_table = 'comercio_ciiu3'
            export_standar_name = Export_CIIU3
            import_standar_table = 'comercio_export_ciiu3'
            import_standar_name = Import_CIIU3
            import_standar_table = 'comercio_import_ciiu3'
        elif standar == '4':
            standar_name = CPC
            standar_table = 'comercio_cpc'
            export_standar_name = Export_CPC
            import_standar_table = 'comercio_export_cpc'
            import_standar_name = Import_CPC
            import_standar_table = 'comercio_import_cpc'
        elif standar == '5':
            standar_name = CUODE
            standar_table = 'comercio_cuode'
            export_standar_name = Export_CUODE
            import_standar_table = 'comercio_export_cuode'
            import_standar_name = Import_CUODE
            import_standar_table = 'comercio_import_cuode'

    data_result = []
    data_table_A = []

    table_A = sql_A(standar_name, standar_table, standar_codigo, value_A, value_B)

    if standar == '1':
        for va in table_A:
            data_table_A.append([va.subpartida, va.descripcion])
    else:
        for va in table_A:
            data_table_A.append([va.codigo, va.descripcion])

    data_result.append([data_table_A])

    data_table_B = []

    # table_B = sql_B()


    message = json.dumps(data_result)
    return HttpResponse(message, content_type='application/json')


#standar_name: NANDINA, CGCE, CPC, CUODE, CIIU3 (objetos)
#standar_table: comercio_nandina, comercio_cgce, comercio_cpc, comercio_cuode, comercio_ciiu3 (nombre propio de la base)
#standar_clase: subpartida o codigo
#value_A: patron% o null segun 'BuscarPor'
#value_B: patron% o null segun 'BuscarPor'
def sql_A(standar_name, standar_table, standar_clase, value_A, value_B):
    raw_body = ("SELECT * FROM %s WHERE %s ") % (standar_table, standar_codigo)
    raw_where = ("LIKE %s OR descripcion LIKE %s")
    data = standar_name.objects.raw(raw_body+raw_where, [value_A, value_B])
    return data


#standar_name: NANDINA, CGCE, CPC, CUODE, CIIU3 (objetos)
#standar_table: comercio_nandina, comercio_cgce, comercio_cpc, comercio_cuode, comercio_ciiu3 (nombre propio de la base)
#standar_clase: subpartida o codigo
#periodicidad: mes, trimestre, semestre, anual
#value_A: patron% o null segun 'BuscarPor'
#value_B: patron% o null segun 'BuscarPor'
#agreg: # nivel de agregacion
#ini_date: desde.substring(0,4)
#fin_date: hasta.substring(0,4)
def sql_B(tipo, standar_name, standar_table, standar_clase, periodicidad, value_A, value_B, agreg, ini_date, fin_date):
    if(tipo=='export' and periodicidad=="mes"):
        print 'en espera'
        # raw_body = ("SELECT * FROM %s WHERE %s ") % (standar_table, standar_codigo)
        # raw_where = ("LIKE %s OR descripcion LIKE %s")
        # data = standar_name.objects.raw(raw_body+raw_where, [value_A, value_B])
    return data
    # pass



# Export Nandina por mes

# SELECT substr(ifnull(date(EXPORT_NANDINA.ANO || '-0' || EXPORT_NANDINA.MES || '-01', 'utc'),
# date(EXPORT_NANDINA.ANO || '-' || EXPORT_NANDINA.MES || '-01', 'utc')),1,7) AS FECHA,
# substr(EXPORT_NANDINA.SUBPARTIDA_NANDINA,1,@AGREG) AS SUBPARTIDA,
# sum(EXPORT_NANDINA.PESO) AS PESO,
# sum(EXPORT_NANDINA.FOB) AS SUBTOTAL_FOB
# FROM EXPORT_NANDINA
# WHERE (EXPORT_NANDINA.SUBPARTIDA_KEY IN
# (SELECT NANDINA.SUBPARTIDA FROM NANDINA
# WHERE (NANDINA.SUBPARTIDA LIKE @VALUE_A) OR (NANDINA.DESCRIPCION LIKE @VALUE_B)))
# GROUP BY EXPORT_NANDINA.ANO,EXPORT_NANDINA.MES,substr(EXPORT_NANDINA.SUBPARTIDA_NANDINA,1,@AGREG)
# HAVING (FECHA>=@INI_DATE) AND (FECHA<=@FIN_DATE)



# Expot CPC por mes

# SELECT substr(ifnull(date(EXPORT_CPC.ANO || '-0' || EXPORT_CPC.MES || '-01', 'utc'),
# date(EXPORT_CPC.ANO || '-' || EXPORT_CPC.MES || '-01', 'utc'))1,7) AS FECHA,
# substr(EXPORT_CPC.CODIGO,1,@AGREG) AS CODIGO,
# sum(EXPORT_CPC.PESO) AS PESO,
# sum(EXPORT_CPC.FOB) AS SUBTOTAL_FOB
# FROM EXPORT_CPC
# WHERE (EXPORT_CPC.CODIGO IN
# (SELECT CPC.CODIGO FROM CPC
# WHERE (CPC.CODIGO LIKE @VALUE_A) OR (CPC.DESCRIPCION LIKE @VALUE_B)))
# GROUP BY EXPORT_CPC.ANO,EXPORT_CPC.MES,substr(EXPORT_CPC.CODIGO,1,@AGREG)
# HAVING (FECHA>=@INI_DATE) AND (FECHA<=@FIN_DATE)