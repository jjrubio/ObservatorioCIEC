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

    print checkbox_pais

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
        table_B = sql_B_clase(tipo, tipo_standar_name, tipo_standar_table, standar_name, standar_table, standar_clase,
                                        standar_var1, standar_var2, period, value_A, value_B, agreg, ini_date, fin_date, checkbox_pais)
    else:
        table_B = sql_B_pais(tipo, tipo_standar_name, tipo_standar_table, standar_name, standar_table, standar_clase,
                                        standar_var1, standar_var2, period, value, agreg, ini_date, fin_date)

    print table_B
    for vb in table_B:
        print vb
        print vb.subpartida
        print vb.PESO
        print vb.SUBTOTAL_FOB
            # data_table_A.append([va.codigo, va.descripcion])

    message = json.dumps(data_result)
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
def sql_B_clase(tipo, tipo_standar_name, tipo_standar_table, standar_name, standar_table, standar_clase,
                        standar_var1, standar_var2, period, value_A, value_B, agreg, ini_date, fin_date, checkbox_pais):
    a = '%'+'a'
    b = '%'+'ot'+'%'
    if(tipo=='1' and period=='1'):
        raw_body = ("""SELECT id, substr(ifnull(date(concat(ANO,'-0',MES,'-01')),date(concat(ANO,'-',MES,'-01'))),1,7) AS FECHA,
                                substr(%s,1,%s) AS %s,
                                sum(peso) AS PESO,
                                sum(fob) AS SUBTOTAL_FOB
                                FROM %s
                                # WHERE (%s IN
                                # (SELECT comercio_nandina.subpartida FROM comercio_nandina

                                """) % (standar_var1, agreg, standar_clase, tipo_standar_table)
                                #         WHERE (%s IN
                                # (SELECT %s FROM %s
                                # WHERE (comercio_nandina.subpartida = '10111') OR (comercio_nandina.descripcion = '12223')))""") % (standar_var1, agreg, standar_clase, type_standar_table, standar_var2, standar_clase, standar_table)

        raw_where = ("WHERE (comercio_nandina.subpartida LIKE %s) OR (comercio_nandina.descripcion LIKE %s))) ")
        # table_B = tipo_standar_name.objects.raw(raw_body)
        table_B = tipo_standar_name.objects.raw(raw_body + raw_where, [a, b])

    return table_B


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



def sql_B_pais(tipo, standar_name, standar_table, standar_clase, periodicidad, value, agreg, ini_date, fin_date):
    if(tipo=='1' and periodicidad=='1'):
        print 'en espera'
        raw_body = ("SELECT id"
                            "FROM comercio_export_nandina") % (standar_table, standar_table)
        # raw_where = ("LIKE %s OR descripcion LIKE %s")
        table_B = standar_name.objects.raw(raw_body, [value_A, value_B])
    return table_B





#standar_name: NANDINA, CGCE, CPC, CUODE, CIIU3
#standar_table: comercio_nandina, comercio_cgce, comercio_cpc, comercio_cuode, comercio_ciiu3
#standar_clase: subpartida o codigo
def sql_C(standar_name, standar_table, standar_clase, standar_codigo, codigo_estandar_request, standar_equivalencia):
    raw_body = ("SELECT * FROM %s INNER JOIN %s ON %s.subpartida=%s.nandina WHERE %s.") % (standar_table, standar_equivalencia, standar_table, standar_equivalencia, standar_equivalencia)
    raw_where = ("cgce=%s")
    # raw_where = ("ciiu3=codigo_estandar_request")
    # raw_where = ("cpc=codigo_estandar_request")
    # raw_where = ("cuode=codigo_estandar_request")
    data = standar_name.objects.raw(raw_body+raw_where,[codigo_estandar_request])
    return data

def sql_D(tipo, export_standar_name, export_standar_table, standar_table, agreg, value_A, value_B, ini_date, fin_date, codigo_estandar_request):
    if(tipo==1):
        raw_body_A = ("SELECT id, %s.ano AS ANO, substr(%s.codigo,1,%s) AS CODIGO, sum(%s.peso) AS PESO, sum(%s.fob) AS SUBTOTAL_FOB FROM %s WHERE (%s.") %(export_standar_table, export_standar_table, agreg,export_standar_table, export_standar_table, export_standar_table, export_standar_table)
        raw_where_A = ("codigo IN (")
        raw_body_B = ("SELECT %s.codigo FROM %s WHERE (%s.codigo ") %(standar_table, standar_table, standar_table)
        #raw_where_B = ("LIKE %s) OR (descripcion LIKE %s))) GROUP BY %s.ano, substr(%s.codigo,1,%s) HAVING(ANO>=%s) AND (ANO<=%s)")
        raw_where_B = ("LIKE %s) OR (descripcion LIKE %s))) GROUP BY ANO HAVING(ANO>=%s) AND (ANO<=%s)")
        data = export_standar_name.objects.raw(raw_body_A+raw_where_A+raw_body_B+raw_where_B, [value_A, value_B, ini_date, fin_date])
    else:
        raw_body_A = ("SELECT id, %s.ano AS ANO, substr(%s.subpartida_nandina,1,%s) AS SUBPARTIDA, sum(%s.peso) AS PESO, sum(%s.fob) AS SUBTOTAL_FOB FROM %s WHERE (%s.") %(export_standar_table, export_standar_table, agreg,export_standar_table, export_standar_table, export_standar_table, export_standar_table)
        raw_where_A = ("subpartida_key IN (")
        raw_body_B = ("SELECT %s.subpartida FROM %s WHERE (%s.subpartida ") %(standar_table, standar_table, standar_table)
        #raw_where_B = ("LIKE %s) OR (descripcion LIKE %s))) GROUP BY %s.ano, substr(%s.codigo,1,%s) HAVING(ANO>=%s) AND (ANO<=%s)")
        raw_where_B = ("LIKE %s) OR (descripcion LIKE %s))) GROUP BY ANO HAVING(ANO>=%s) AND (ANO<=%s)")
        data = export_standar_name.objects.raw(raw_body_A+raw_where_A+raw_body_B+raw_where_B, [value_A, value_B, ini_date, fin_date])

    return data

def sql_E(tipo, export_standar_name, export_standar_table, standar_table, pais_tabla, agreg, value_A, value_B, ini_date, fin_date):
    #falta agregar substr al fina antes del having
    if(tipo==1):
        raw_body_A = ("SELECT %s.id, %s.ano AS ANO, %s.pais, substr(%s.codigo,1,%s) AS CODIGO, sum(%s.peso) AS PESO, sum(%s.fob) AS SUBTOTAL_FOB FROM %s INNER JOIN %s ON (%s.codigo=%s.pais) WHERE (%s.") %(export_standar_table, export_standar_table, pais_tabla, export_standar_table, agreg, export_standar_table, export_standar_table, export_standar_table, pais_tabla, pais_tabla, export_standar_table, export_standar_table)
        raw_where_A = ("codigo IN (")
        raw_body_B = ("SELECT %s.codigo FROM %s WHERE (%s.codigo ") %(standar_table, standar_table, standar_table)
        raw_where_B = ("LIKE %s) OR  (descripcion LIKE %s))) GROUP BY ANO, PAIS HAVING(ANO>=%s) AND (ANO<=%s)")
        data = export_standar_name.objects.raw(raw_body_A+raw_where_A+raw_body_B+raw_where_B, [value_A,value_B,ini_date,fin_date])
    else:
        raw_body_A = ("SELECT %s.id, %s.ano AS ANO, %s.pais, substr(%s.subpartida_nandina,1,%s) AS SUBPARTIDA, sum(%s.peso) AS PESO, sum(%s.fob) AS SUBTOTAL_FOB FROM %s INNER JOIN %s ON (%s.codigo=%s.pais) WHERE (%s.") %(export_standar_table, export_standar_table, pais_tabla, export_standar_table, agreg, export_standar_table, export_standar_table, export_standar_table, pais_tabla, pais_tabla, export_standar_table, export_standar_table)
        raw_where_A = ("subpartida_key IN (")
        raw_body_B = ("SELECT %s.subpartida FROM %s WHERE (%s.subpartida ") %(standar_table, standar_table, standar_table)
        raw_where_B = ("LIKE %s) OR  (descripcion LIKE %s))) GROUP BY ANO, PAIS HAVING(ANO>=%s) AND (ANO<=%s)")
        data = export_standar_name.objects.raw(raw_body_A+raw_where_A+raw_body_B+raw_where_B, [value_A,value_B,ini_date,fin_date])

    return data

def sql_F(tipo, export_standar_name, export_standar_table, standar_table, pais_tabla, agreg, value_A, ini_date, fin_date):
    #falta agregar substr al final antes del having
    if (tipo == 1):
        raw_body_A = ("SELECT %s.id, %s.ano AS ANO, %s.pais, substr(%s.codigo,1,%s) AS CODIGO, sum(%s.peso) AS PESO, sum(%s.fob) AS SUBTOTAL_FOB FROM %s INNER JOIN %s ON %s.codigo=%s.pais WHERE (%s.") %(export_standar_table, export_standar_table, pais_tabla, export_standar_table, agreg, export_standar_table, export_standar_table, export_standar_table, pais_tabla, pais_tabla, export_standar_table, export_standar_table)
        raw_where_A = ("pais IN (")
        raw_body_B = ("SELECT %s.codigo FROM %s WHERE (%s.pais ") %(pais_tabla, pais_tabla, pais_tabla)
        raw_where_B = ("LIKE %s))) GROUP BY ANO, PAIS HAVING(ANO>=%s) AND (ANO<=%s)")
        data = export_standar_name.objects.raw(raw_body_A+raw_where_A+raw_body_B+raw_where_B, [value_A,ini_date,fin_date])
    else:
        raw_body_A = ("SELECT %s.id, %s.ano AS ANO, %s.pais, substr(%s.subpartida_nandina,1,%s) AS SUBPARTIDA, sum(%s.peso) AS PESO, sum(%s.fob) AS SUBTOTAL_FOB FROM %s INNER JOIN %s ON %s.codigo=%s.pais WHERE (%s.") %(export_standar_table, export_standar_table, pais_tabla, export_standar_table, agreg, export_standar_table, export_standar_table, export_standar_table, pais_tabla, pais_tabla, export_standar_table, export_standar_table)
        raw_where_A = ("pais IN (")
        raw_body_B = ("SELECT %s.codigo FROM %s WHERE (%s.pais ") %(pais_tabla, pais_tabla, pais_tabla)
        raw_where_B = ("LIKE %s))) GROUP BY ANO, PAIS HAVING(ANO>=%s) AND (ANO<=%s)")
        data = export_standar_name.objects.raw(raw_body_A+raw_where_A+raw_body_B+raw_where_B, [value_A,ini_date,fin_date])

    return data

def sql_G(export_standar_name, export_standar_table, standar_table, value_A, value_B):
    # falta el where fecha y falta el substr para el group by
    #data = Export_CUODE.objects.raw("SELECT V_TABLE.id, V_TABLE.ANO || '-0' || V_TABLE.SEMESTRE AS FECHA, V_TABLE.CODIGO AS CODIGO, V_TABLE.PESO AS PESO, V_TABLE.SUBTOTAL_FOB AS SUBTOTAL_FOB 
    #FROM (SELECT comercio_export_cuode.id, comercio_export_cuode.ano AS ANO, ((comercio_export_cuode.MES-1)/6)+1 AS SEMESTRE, substr(comercio_export_cuode.codigo,1,1) AS CODIGO, sum(comercio_export_cuode.peso) AS PESO, sum(comercio_export_cuode.fob) AS SUBTOTAL_FOB FROM comercio_export_cuode 
    #WHERE (comercio_export_cuode.codigo IN (SELECT comercio_cuode.codigo FROM comercio_cuode 
    #WHERE (comercio_cuode.codigo LIKE %s) OR (comercio_cuode.descripcion LIKE NULL))) GROUP BY ANO, SEMESTRE, substr(comercio_export_cuode.codigo,1,1)) AS V_TABLE LIMIT 20", [var])
    print 'aqui'
    agreg = 1
    ini_date = '1990-01'
    fin_date = '1991-01'
    
    #PARA CGCE, CPC, CUODE Y CIIU3
    raw_body_A = ("SELECT V_TABLE.id, CONCAT(ANO,'-0',FLOOR(SEMESTRE)) AS FECHA, V_TABLE.CODIGO AS CODIGO, V_TABLE.PESO AS PESO, V_TABLE.SUBTOTAL_FOB AS SUBTOTAL_FOB FROM(")
    raw_body_B = ("SELECT %s.id, %s.ano AS ANO, ((%s.MES-1)/6)+1 AS SEMESTRE, substr(%s.codigo,1,%s) AS CODIGO, sum(%s.peso) AS PESO, sum(%s.fob) AS SUBTOTAL_FOB FROM %s WHERE (%s.") %(export_standar_table,export_standar_table,export_standar_table,export_standar_table,agreg,export_standar_table,export_standar_table,export_standar_table,export_standar_table)
    raw_where_A = ("codigo IN (")
    raw_body_C = ("SELECT %s.codigo FROM %s WHERE (%s.") %(standar_table,standar_table,standar_table)
    raw_where_B = ("codigo LIKE %s) OR (descripcion LIKE %s))) ")
    raw_group_by_A = ("GROUP BY ANO, SEMESTRE) AS V_TABLE")
    data = export_standar_name.objects.raw(raw_body_A+raw_body_B+raw_where_A+raw_body_C+raw_where_B+raw_group_by_A, [value_A, value_B])
    
    #PARA NANDINA
    raw_body_A = ("SELECT V_TABLE.id, CONCAT(ANO,'-0',FLOOR(SEMESTRE)) AS FECHA, V_TABLE.SUBPARTIDA AS SUBPARTIDA, V_TABLE.PESO AS PESO, V_TABLE.SUBTOTAL_FOB AS SUBTOTAL_FOB FROM(")
    raw_body_B = ("SELECT %s.id, %s.ano AS ANO, ((%s.MES-1)/6)+1 AS SEMESTRE, substr(%s.subpartida_nandina,1,%s) AS SUBPARTIDA, sum(%s.peso) AS PESO, sum(%s.fob) AS SUBTOTAL_FOB FROM %s WHERE (%s.") %(export_standar_table,export_standar_table,export_standar_table,export_standar_table,agreg,export_standar_table,export_standar_table,export_standar_table,export_standar_table)
    raw_where_A = ("subpartida_key IN (")
    raw_body_C = ("SELECT %s.subpartida FROM %s WHERE (%s.") %(standar_table,standar_table,standar_table)
    raw_where_B = ("subpartida LIKE %s) OR (descripcion LIKE %s))) ")
    raw_group_by_A = ("GROUP BY ANO, SEMESTRE) AS V_TABLE")
    data = export_standar_name.objects.raw(raw_body_A+raw_body_B+raw_where_A+raw_body_C+raw_where_B+raw_group_by_A, [value_A, value_B])

    return data

def sql_H(export_standar_name, export_standar_table, standar_table, value_A, value_B):
    # falta el where fecha y falta el substr para el group by
    #data = Export_CUODE.objects.raw("SELECT V_TABLE.id, V_TABLE.ANO || '-0' || V_TABLE.SEMESTRE AS FECHA, V_TABLE.CODIGO AS CODIGO, V_TABLE.PESO AS PESO, V_TABLE.SUBTOTAL_FOB AS SUBTOTAL_FOB 
    #FROM (SELECT comercio_export_cuode.id, comercio_export_cuode.ano AS ANO, ((comercio_export_cuode.MES-1)/6)+1 AS SEMESTRE, substr(comercio_export_cuode.codigo,1,1) AS CODIGO, sum(comercio_export_cuode.peso) AS PESO, sum(comercio_export_cuode.fob) AS SUBTOTAL_FOB FROM comercio_export_cuode 
    #WHERE (comercio_export_cuode.codigo IN (SELECT comercio_cuode.codigo FROM comercio_cuode 
    #WHERE (comercio_cuode.codigo LIKE %s) OR (comercio_cuode.descripcion LIKE NULL))) GROUP BY ANO, SEMESTRE, substr(comercio_export_cuode.codigo,1,1)) AS V_TABLE LIMIT 20", [var])
    agreg = 1
    ini_date = '1990-01'
    fin_date = '1991-01'
    
    #PARA CGCE, CPC, CUODE Y CIIU3
    raw_body_A = ("SELECT V_TABLE.id, CONCAT(ANO,'-0',FLOOR(SEMESTRE)) AS FECHA, V_TABLE.CODIGO AS CODIGO, V_TABLE.PESO AS PESO, V_TABLE.SUBTOTAL_FOB AS SUBTOTAL_FOB FROM(")
    raw_body_B = ("SELECT %s.id, %s.ano AS ANO, ((%s.MES-1)/3)+1 AS SEMESTRE, substr(%s.codigo,1,%s) AS CODIGO, sum(%s.peso) AS PESO, sum(%s.fob) AS SUBTOTAL_FOB FROM %s WHERE (%s.") %(export_standar_table,export_standar_table,export_standar_table,export_standar_table,agreg,export_standar_table,export_standar_table,export_standar_table,export_standar_table)
    raw_where_A = ("codigo IN (")
    raw_body_C = ("SELECT %s.codigo FROM %s WHERE (%s.") %(standar_table,standar_table,standar_table)
    raw_where_B = ("codigo LIKE %s) OR (descripcion LIKE %s))) ")
    raw_group_by_A = ("GROUP BY ANO, SEMESTRE) AS V_TABLE")
    data = export_standar_name.objects.raw(raw_body_A+raw_body_B+raw_where_A+raw_body_C+raw_where_B+raw_group_by_A, [value_A, value_B])
    
    #PARA NANDINA
    raw_body_A = ("SELECT V_TABLE.id, CONCAT(ANO,'-0',FLOOR(SEMESTRE)) AS FECHA, V_TABLE.SUBPARTIDA AS SUBPARTIDA, V_TABLE.PESO AS PESO, V_TABLE.SUBTOTAL_FOB AS SUBTOTAL_FOB FROM(")
    raw_body_B = ("SELECT %s.id, %s.ano AS ANO, ((%s.MES-1)/3)+1 AS SEMESTRE, substr(%s.subpartida_nandina,1,%s) AS SUBPARTIDA, sum(%s.peso) AS PESO, sum(%s.fob) AS SUBTOTAL_FOB FROM %s WHERE (%s.") %(export_standar_table,export_standar_table,export_standar_table,export_standar_table,agreg,export_standar_table,export_standar_table,export_standar_table,export_standar_table)
    raw_where_A = ("subpartida_key IN (")
    raw_body_C = ("SELECT %s.subpartida FROM %s WHERE (%s.") %(standar_table,standar_table,standar_table)
    raw_where_B = ("subpartida LIKE %s) OR (descripcion LIKE %s))) ")
    raw_group_by_A = ("GROUP BY ANO, SEMESTRE) AS V_TABLE")
    data = export_standar_name.objects.raw(raw_body_A+raw_body_B+raw_where_A+raw_body_C+raw_where_B+raw_group_by_A, [value_A, value_B])

    return data

def sql_I(export_standar_name, export_standar_table, standar_table, value_A, value_B):

    agreg = 1
    ini_date = '1990-01'
    fin_date = '1991-01'
    tabla_pais = 'comercio_paises'

    #group by substr y pais, agregar tb el where de fecha

    #data = Export_CUODE.objects.raw("SELECT V_TABLE.id, CONCAT(ANO,'-0',FLOOR(SEMESTRE)) AS FECHA, V_TABLE.PAIS AS PAIS, V_TABLE.CODIGO AS CODIGO, V_TABLE.PESO AS PESO, V_TABLE.SUBTOTAL_FOB AS SUBTOTAL_FOB FROM 
    #(SELECT comercio_export_cuode.id, comercio_export_cuode.ano AS ANO, ((comercio_export_cuode.MES-1)/6)+1 AS SEMESTRE, comercio_paises.pais AS PAIS, substr(comercio_export_cuode.codigo,1,1) AS CODIGO, sum(comercio_export_cuode.peso) AS PESO, sum(comercio_export_cuode.fob) AS SUBTOTAL_FOB FROM comercio_export_cuode INNER JOIN comercio_paises ON (comercio_paises.codigo=comercio_export_cuode.pais) 
    #WHERE (comercio_export_cuode.pais IN(
    #SELECT comercio_paises.codigo FROM comercio_paises WHERE (comercio_paises.pais LIKE %s))) 
    #GROUP BY ANO, SEMESTRE, PAIS) AS V_TABLE", [var])
    
    #PARA CGCE, CPC, CUODE Y CIIU3
    raw_body_A = ("SELECT V_TABLE.id, CONCAT(ANO,'-0',FLOOR(SEMESTRE)) AS FECHA, V_TABLE.PAIS AS PAIS,V_TABLE.CODIGO AS CODIGO, V_TABLE.PESO AS PESO, V_TABLE.SUBTOTAL_FOB AS SUBTOTAL_FOB FROM(")
    raw_body_B = ("SELECT %s.id, %s.ano AS ANO, ((%s.MES-1)/6)+1 AS SEMESTRE, %s.pais AS PAIS, substr(%s.codigo,1,%s) AS CODIGO, sum(%s.peso) AS PESO, sum(%s.fob) AS SUBTOTAL_FOB FROM %s INNER JOIN %s ON %s.codigo=%s.pais WHERE (%s.") %(export_standar_table,export_standar_table,export_standar_table, tabla_pais,export_standar_table,agreg,export_standar_table,export_standar_table,export_standar_table,tabla_pais, tabla_pais,export_standar_table,export_standar_table)
    raw_where_A = ("pais IN (")
    raw_body_C = ("SELECT %s.codigo FROM %s WHERE (%s.") %(tabla_pais,tabla_pais,tabla_pais)
    raw_where_B = ("pais LIKE %s))) ")
    raw_group_by_A = ("GROUP BY ANO, SEMESTRE) AS V_TABLE")
    data = export_standar_name.objects.raw(raw_body_A+raw_body_B+raw_where_A+raw_body_C+raw_where_B+raw_group_by_A, [value_A])
    
    #PARA NANDINA
    raw_body_A = ("SELECT V_TABLE.id, CONCAT(ANO,'-0',FLOOR(SEMESTRE)) AS FECHA, V_TABLE.PAIS AS PAIS,V_TABLE.SUBPARTIDA AS SUBPARTIDA, V_TABLE.PESO AS PESO, V_TABLE.SUBTOTAL_FOB AS SUBTOTAL_FOB FROM(")
    raw_body_B = ("SELECT %s.id, %s.ano AS ANO, ((%s.MES-1)/6)+1 AS SEMESTRE, %s.pais AS PAIS, substr(%s.subpartida_nandina,1,%s) AS SUBPARTIDA, sum(%s.peso) AS PESO, sum(%s.fob) AS SUBTOTAL_FOB FROM %s INNER JOIN %s ON %s.codigo=%s.pais WHERE (%s.") %(export_standar_table,export_standar_table,export_standar_table, tabla_pais,export_standar_table,agreg,export_standar_table,export_standar_table,export_standar_table,tabla_pais, tabla_pais,export_standar_table,export_standar_table)
    raw_where_A = ("pais IN (")
    raw_body_C = ("SELECT %s.codigo FROM %s WHERE (%s.") %(tabla_pais,tabla_pais,tabla_pais)
    raw_where_B = ("pais LIKE %s))) ")
    raw_group_by_A = ("GROUP BY ANO, SEMESTRE) AS V_TABLE")
    data = export_standar_name.objects.raw(raw_body_A+raw_body_B+raw_where_A+raw_body_C+raw_where_B+raw_group_by_A, [value_A])

    return data

def sql_J(export_standar_name, export_standar_table, standar_table, value_A, value_B):

    agreg = 1
    ini_date = '1990-01'
    fin_date = '1991-01'
    tabla_pais = 'comercio_paises'

    #group by substr y pais, agregar tb el where de fecha

    #data = Export_CUODE.objects.raw("SELECT V_TABLE.id, CONCAT(ANO,'-0',FLOOR(SEMESTRE)) AS FECHA, V_TABLE.PAIS AS PAIS, V_TABLE.CODIGO AS CODIGO, V_TABLE.PESO AS PESO, V_TABLE.SUBTOTAL_FOB AS SUBTOTAL_FOB FROM 
    #(SELECT comercio_export_cuode.id, comercio_export_cuode.ano AS ANO, ((comercio_export_cuode.MES-1)/6)+1 AS SEMESTRE, comercio_paises.pais AS PAIS, substr(comercio_export_cuode.codigo,1,1) AS CODIGO, sum(comercio_export_cuode.peso) AS PESO, sum(comercio_export_cuode.fob) AS SUBTOTAL_FOB FROM comercio_export_cuode INNER JOIN comercio_paises ON (comercio_paises.codigo=comercio_export_cuode.pais) 
    #WHERE (comercio_export_cuode.pais IN(
    #SELECT comercio_paises.codigo FROM comercio_paises WHERE (comercio_paises.pais LIKE %s))) 
    #GROUP BY ANO, SEMESTRE, PAIS) AS V_TABLE", [var])
    
    #PARA CGCE, CPC, CUODE Y CIIU3
    raw_body_A = ("SELECT V_TABLE.id, CONCAT(ANO,'-0',FLOOR(SEMESTRE)) AS FECHA, V_TABLE.PAIS AS PAIS,V_TABLE.CODIGO AS CODIGO, V_TABLE.PESO AS PESO, V_TABLE.SUBTOTAL_FOB AS SUBTOTAL_FOB FROM(")
    raw_body_B = ("SELECT %s.id, %s.ano AS ANO, ((%s.MES-1)/6)+1 AS SEMESTRE, %s.pais AS PAIS, substr(%s.codigo,1,%s) AS CODIGO, sum(%s.peso) AS PESO, sum(%s.fob) AS SUBTOTAL_FOB FROM %s INNER JOIN %s ON %s.codigo=%s.pais WHERE (%s.") %(export_standar_table,export_standar_table,export_standar_table, tabla_pais,export_standar_table,agreg,export_standar_table,export_standar_table,export_standar_table,tabla_pais, tabla_pais,export_standar_table,export_standar_table)
    raw_where_A = ("codigo IN (")
    raw_body_C = ("SELECT %s.codigo FROM %s WHERE (%s.") %(export_standar_table,export_standar_table,export_standar_table)
    raw_where_B = ("codigo LIKE %s) OR (descripcion LIKE %s))) ")
    raw_group_by_A = ("GROUP BY ANO, SEMESTRE) AS V_TABLE")
    data = export_standar_name.objects.raw(raw_body_A+raw_body_B+raw_where_A+raw_body_C+raw_where_B+raw_group_by_A, [value_A,value_B])
    
    #PARA NANDINA
    raw_body_A = ("SELECT V_TABLE.id, CONCAT(ANO,'-0',FLOOR(SEMESTRE)) AS FECHA, V_TABLE.PAIS AS PAIS,V_TABLE.SUBPARTIDA AS SUBPARTIDA, V_TABLE.PESO AS PESO, V_TABLE.SUBTOTAL_FOB AS SUBTOTAL_FOB FROM(")
    raw_body_B = ("SELECT %s.id, %s.ano AS ANO, ((%s.MES-1)/6)+1 AS SEMESTRE, %s.pais AS PAIS, substr(%s.subpartida_nandina,1,%s) AS SUBPARTIDA, sum(%s.peso) AS PESO, sum(%s.fob) AS SUBTOTAL_FOB FROM %s INNER JOIN %s ON %s.codigo=%s.pais WHERE (%s.") %(export_standar_table,export_standar_table,export_standar_table, tabla_pais,export_standar_table,agreg,export_standar_table,export_standar_table,export_standar_table,tabla_pais, tabla_pais,export_standar_table,export_standar_table)
    raw_where_A = ("pais IN (")
    raw_body_C = ("SELECT %s.codigo FROM %s WHERE (%s.") %(export_standar_table,export_standar_table,export_standar_table)
    raw_where_B = ("pais LIKE %s) OR (descripcion LIKE %s))) ")
    raw_group_by_A = ("GROUP BY ANO, SEMESTRE) AS V_TABLE")
    data = export_standar_name.objects.raw(raw_body_A+raw_body_B+raw_where_A+raw_body_C+raw_where_B+raw_group_by_A, [value_A,value_B])

    return data

def sql_K(export_standar_name, export_standar_table, standar_table, value_A, value_B):

    agreg = 1
    ini_date = '1990-01'
    fin_date = '1991-01'
    tabla_pais = 'comercio_paises'

    #group by substr y pais, agregar tb el where de fecha

    #data = Export_CUODE.objects.raw("SELECT V_TABLE.id, CONCAT(ANO,'-0',FLOOR(SEMESTRE)) AS FECHA, V_TABLE.PAIS AS PAIS, V_TABLE.CODIGO AS CODIGO, V_TABLE.PESO AS PESO, V_TABLE.SUBTOTAL_FOB AS SUBTOTAL_FOB FROM 
    #(SELECT comercio_export_cuode.id, comercio_export_cuode.ano AS ANO, ((comercio_export_cuode.MES-1)/6)+1 AS SEMESTRE, comercio_paises.pais AS PAIS, substr(comercio_export_cuode.codigo,1,1) AS CODIGO, sum(comercio_export_cuode.peso) AS PESO, sum(comercio_export_cuode.fob) AS SUBTOTAL_FOB FROM comercio_export_cuode INNER JOIN comercio_paises ON (comercio_paises.codigo=comercio_export_cuode.pais) 
    #WHERE (comercio_export_cuode.pais IN(
    #SELECT comercio_paises.codigo FROM comercio_paises WHERE (comercio_paises.pais LIKE %s))) 
    #GROUP BY ANO, SEMESTRE, PAIS) AS V_TABLE", [var])
    
    #PARA CGCE, CPC, CUODE Y CIIU3
    raw_body_A = ("SELECT V_TABLE.id, CONCAT(ANO,'-0',FLOOR(SEMESTRE)) AS FECHA, V_TABLE.PAIS AS PAIS,V_TABLE.CODIGO AS CODIGO, V_TABLE.PESO AS PESO, V_TABLE.SUBTOTAL_FOB AS SUBTOTAL_FOB FROM(")
    raw_body_B = ("SELECT %s.id, %s.ano AS ANO, ((%s.MES-1)/3)+1 AS SEMESTRE, %s.pais AS PAIS, substr(%s.codigo,1,%s) AS CODIGO, sum(%s.peso) AS PESO, sum(%s.fob) AS SUBTOTAL_FOB FROM %s INNER JOIN %s ON %s.codigo=%s.pais WHERE (%s.") %(export_standar_table,export_standar_table,export_standar_table, tabla_pais,export_standar_table,agreg,export_standar_table,export_standar_table,export_standar_table,tabla_pais, tabla_pais,export_standar_table,export_standar_table)
    raw_where_A = ("codigo IN (")
    raw_body_C = ("SELECT %s.codigo FROM %s WHERE (%s.") %(export_standar_table,export_standar_table,export_standar_table)
    raw_where_B = ("codigo LIKE %s) OR (descripcion LIKE %s))) ")
    raw_group_by_A = ("GROUP BY ANO, SEMESTRE) AS V_TABLE")
    data = export_standar_name.objects.raw(raw_body_A+raw_body_B+raw_where_A+raw_body_C+raw_where_B+raw_group_by_A, [value_A,value_B])
    
    #PARA NANDINA
    raw_body_A = ("SELECT V_TABLE.id, CONCAT(ANO,'-0',FLOOR(SEMESTRE)) AS FECHA, V_TABLE.PAIS AS PAIS,V_TABLE.SUBPARTIDA AS SUBPARTIDA, V_TABLE.PESO AS PESO, V_TABLE.SUBTOTAL_FOB AS SUBTOTAL_FOB FROM(")
    raw_body_B = ("SELECT %s.id, %s.ano AS ANO, ((%s.MES-1)/3)+1 AS SEMESTRE, %s.pais AS PAIS, substr(%s.subpartida_nandina,1,%s) AS SUBPARTIDA, sum(%s.peso) AS PESO, sum(%s.fob) AS SUBTOTAL_FOB FROM %s INNER JOIN %s ON %s.codigo=%s.pais WHERE (%s.") %(export_standar_table,export_standar_table,export_standar_table, tabla_pais,export_standar_table,agreg,export_standar_table,export_standar_table,export_standar_table,tabla_pais, tabla_pais,export_standar_table,export_standar_table)
    raw_where_A = ("pais IN (")
    raw_body_C = ("SELECT %s.codigo FROM %s WHERE (%s.") %(export_standar_table,export_standar_table,export_standar_table)
    raw_where_B = ("pais LIKE %s) OR (descripcion LIKE %s))) ")
    raw_group_by_A = ("GROUP BY ANO, SEMESTRE) AS V_TABLE")
    data = export_standar_name.objects.raw(raw_body_A+raw_body_B+raw_where_A+raw_body_C+raw_where_B+raw_group_by_A, [value_A,value_B])

    return data

def sql_D_2(import_standar_name, import_standar_table, standar_table, agreg, value_A, value_B, ini_date, fin_date):
    #falta agregar substr al final antes del having

    ini_date = '1990-01'
    fin_date = '1991-01'

    #PARA CGCE, CPC, CUODE Y CIIU3
    raw_body_A = ("SELECT id, %s.ano AS ANO, substr(%s.codigo,1,%s) AS CODIGO, sum(%s.peso) AS PESO, sum(%s.fob) AS SUBTOTAL_FOB, sum(%s.cif) AS SUBTOTAL_CIF FROM %s WHERE (%s.") %(import_standar_table, import_standar_table, agreg,import_standar_table, import_standar_table, import_standar_table, import_standar_table, import_standar_table)
    raw_where_A = ("codigo IN (")
    raw_body_B = ("SELECT %s.codigo FROM %s WHERE (%s.codigo ") %(standar_table, standar_table, standar_table)
    raw_where_B = ("LIKE %s) OR (descripcion LIKE %s))) GROUP BY ANO HAVING(ANO>=%s) AND (ANO<=%s)")
    data = import_standar_name.objects.raw(raw_body_A+raw_where_A+raw_body_B+raw_where_B, [value_A, value_B, ini_date, fin_date])
    
    #PARA NANDINA
    raw_body_A = ("SELECT id, %s.ano AS ANO, substr(%s.subpartida_nandina,1,%s) AS SUBPARTIDA, sum(%s.peso) AS PESO, sum(%s.fob) AS SUBTOTAL_FOB, sum(%s.cif) AS SUBTOTAL_CIF FROM %s WHERE (%s.") %(import_standar_table, import_standar_table, agreg,import_standar_table, import_standar_table, import_standar_table, import_standar_table, import_standar_table)
    raw_where_A = ("subpartida_key IN (")
    raw_body_B = ("SELECT %s.subpartida FROM %s WHERE (%s.subpartida ") %(standar_table, standar_table, standar_table)
    raw_where_B = ("LIKE %s) OR (descripcion LIKE %s))) GROUP BY ANO HAVING(ANO>=%s) AND (ANO<=%s)")
    data = import_standar_name.objects.raw(raw_body_A+raw_where_A+raw_body_B+raw_where_B, [value_A, value_B, ini_date, fin_date])

    return data