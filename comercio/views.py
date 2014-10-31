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

#     SELECT NANDINA.* FROM NANDINA
# WHERE (NANDINA.SUBPARTIDA LIKE @VALUE_A) OR (NANDINA.DESCRIPCION LIKE @VALUE_B)

    db = Nandina
    db_table = "comercio_nandina"
    valueB = '%,%'
    valueA = None
    # d = CGCE.objects.raw('Select * FROM %s', [db_table])

    raw_select_from = (
    "SELECT * "
    "FROM %s "
    ) % (db_table)

    raw_where =(
        "WHERE subpartida LIKE %s OR descripcion LIKE %s"
    )

    d = db.objects.raw(raw_select_from+raw_where, [valueA, valueB])

    # d = CGCE.objects.raw('Select * FROM %s WHERE descripcion LIKE %s', tuple([db_table,value]))
    print d
    for x in d:
        print x
        print x.subpartida, x.descripcion

    # result = sql_A(standar, value_A, value_B)

    # print result
    # print tab_selected+', '+option+', '+search_by+', '+standar+', '+txt_desde+', '+txt_hasta+', '+period+', '+txt_agregacion+', '+checkbox_select
    message = json.dumps(1)
    return HttpResponse(message, content_type='application/json')


#estandar: Nandina, CGCE, CPC, CUODE, CIIU3
#value_A: patron% o null segun 'BuscarPor'
#value_B: patron% o null segun 'BuscarPor'
def sql_A(estandar, value_A, value_B):
    data = Nandina.objects.filter(Q(subpartida=value_A) | Q(descripcion=value_B)) #5 - 9
    return data

#tipo: Si es export/import
#estandar: Nandina, CGCE, CPC, CUODE, CIIU3
#clase: codigo o subpartida
#periodicidad: mes, trimestre, semestre, anual
#value_A: patron% o null segun 'BuscarPor'
#value_B: patron% o null segun 'BuscarPor'
#agreg: nivel de agregacion
#ini_date: desde.substring(0,4)
#fin_date: hasta.substring(0,4)
def sql_B(tipo, estandar, clase, periodicidad, value_A, value_B, agreg, ini_date, fin_date):
    if(tipo=='export' and periodicidad=="mes"):
        print 'fd'

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
