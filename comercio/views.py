from django.shortcuts import render, render_to_response
from django.template.context import RequestContext
from django.template.loader import get_template
from models import *
from django.db.models import Q

def comercio_page(request):
    template = 'comercio.html'
    return render_to_response(template, context_instance = RequestContext(request,locals()))


#estandar: Nandina, CGCE, CPC, CUODE, CIIU3
#value_A: patron% o null segun 'BuscarPor'
#value_B: patron% o null segun 'BuscarPor'
def sql_A(estandar, value_A, value_B):
    estandar.objects.filter(Q(subpartida=value_A) | Q(descripcion=value_B)) #5 - 9
    return 1

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
    # if(tipo=='export' and  clase=='codigo' and periodicidad="mes"):
    #     print "hola"
    return 1

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
