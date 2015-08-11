#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.shortcuts import HttpResponse, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.template.context import RequestContext
from django.contrib import messages
from models import *
from ENEMDU.models import *
from .forms import UploadFileForm
import csv
import os
import subprocess
from subprocess import PIPE, Popen
from os import listdir
from os.path import isfile, join
import json
from json import JSONEncoder

class PythonObjectEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (list, dict, str, unicode, int, float, bool, type(None))):
            return JSONEncoder.default(self, obj)
        return {'_python_object': pickle.dumps(obj)}

def as_python_object(dct):
    if '_python_object' in dct:
        return pickle.loads(str(dct['_python_object']))
    return dct

def insert_data_enemdu(request):
    context = RequestContext(request)
    template = 'insert_data_enemdu.html'
    upload_success = False
    empty = False
    path_dir = '/home/patu/Downloads/ObservatorioCIEC-master/media/csv/'
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
                        dbtable = 'enemdu_data_from_2003_4'
                    else:
                        dbtable = 'enemdu_data_from_2007_2'            
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
                            for i in range(1,len(my_list)):
                                fexp,upm,dominio,dominio2,anio,trimestre,region_natural,area,ciudad_ind,zonaPlanificacion,rela_jef,hombre,edad,edad_group,etnia,genero,nivinst,anosaprob,asisteClases,analfabeta,hablaEspaniol,hablaIndigena,hablaExtranjero,experiencia,haceDeportes,horasDeportes,migracion_extranjera,mig_noprin_prin,mig_prin_noprin,mig_prin_prin,mig_noprin_noprin,tamano_hogar,hogar_noFamiliar,part_quehaceres,horas_part_quehaceres,hogar_completo,ingrl,ingreso_hogar,pobreza,pobreza_extrema,seguro,pet,pei,pea,empleo,desempleo,cesantes,desm_nuevo,semanas_busc_trab,desoNoBusca,grupo_ocup_1,rama_act_2,sect_informal,sect_srvdom,categ_ocupa,tipo_deso,condInact,rentista,jubil,estudiant,amaCasa,incapacit,otro,jefeHogar,oplenos,suboc,suboc1,condact,tipo_ocupa,satis_laboral,descon_bajos_ingresos,descon_horarios,descon_estabil,descon_amb_laboral,descon_activ,sect_formal,nocla_sector,desemab,desemoc,suboc2,sub_informal,sect_moderno,sect_agricola,sub_inv,empleoAdecuado,empleoInadecuado,subempleo,subempleoXhoras,subempleoXingreso,otroEmpleoInadec,empleoNoclasificado,empleoNoremunerado,tipoEmpleo,tipoEmpleoDesag,sectorEmpleo = str(my_list[i]).split(';')
                                fexp_new,value = fexp.split('[')
                                value_coma,wcoma = value.split("'")
                                if sectorEmpleo == "']":
                                    sectorEmpleo = None
                                try:
                                    fexp_float = float(wcoma)
                                except ValueError:
                                    if fexp_float == 0:
                                        pass
                                    else:
                                        files_failed.append(str(afile))
                                        error_find.append('fexp')
                                        break
                                try:
                                    upm_int = int(upm)
                                except ValueError:
                                    if upm_int == 0:
                                        pass
                                    else:
                                        files_failed.append(str(afile))
                                        error_find.append('upm')
                                        break
                                try:
                                    dominio_str = str(dominio)
                                except ValueError:
                                    if dominio_str == 0:
                                        pass
                                    else:
                                        files_failed.append(str(afile))
                                        error_find.append('dominio')
                                        break
                                try:
                                    dominio2_str = str(dominio2)
                                except ValueError:
                                    if dominio2_str == 0:
                                        pass
                                    else:
                                        files_failed.append(str(afile))
                                        error_find.append('dominio2')
                                        break
                                try:
                                    anio_int = int(anio)
                                except ValueError:
                                    if anio_int == 0:
                                        pass
                                    else:
                                        files_failed.append(str(afile))
                                        error_find.append('anio')
                                        break
                                try:
                                    trimestre_int = int(trimestre)
                                except ValueError:
                                    if trimestre_int == 0:
                                        pass
                                    else:
                                        files_failed.append(str(afile))
                                        error_find.append('trimestre')
                                        break
                                try:
                                    region_natural_str = str(region_natural)
                                    if region_natural_str == '1' or region_natural_str == '2' or region_natural_str == '3' or region_natural_str == '4':
                                        files_failed.append(str(afile))
                                        error_find.append('region_natural')
                                        break
                                except ValueError:
                                    if region_natural_str == 0:
                                        pass
                                    else:
                                        files_failed.append(str(afile))
                                        error_find.append('region_natural')
                                        break
                                try:
                                    area_str = str(area)
                                except ValueError:
                                    if area_str == 0:
                                        pass
                                    else:
                                        files_failed.append(str(afile))
                                        error_find.append('area')
                                        break
                                try:
                                    ciudad_ind_str = str(ciudad_ind)
                                except ValueError:
                                    if ciudad_ind_str == 0:
                                        pass
                                    else:
                                        files_failed.append(str(afile))
                                        error_find.append('ciudad_ind')
                                        break
                                try:
                                    zonaPlanificacion_str = str(zonaPlanificacion)
                                except ValueError:
                                    if zonaPlanificacion_str == 0:
                                        pass
                                    else:
                                        files_failed.append(str(afile))
                                        error_find.append('zonaPlanificacion')
                                        break
                                try:
                                    rela_jef_int = int(rela_jef)
                                except ValueError:
                                    if rela_jef_int == 0:
                                        pass
                                    else:
                                        files_failed.append(str(afile))
                                        error_find.append('rela_jef')
                                        break
                                try:
                                    hombre_int = int(hombre)
                                except ValueError:
                                    if hombre_int == 0:
                                        pass
                                    else:
                                        files_failed.append(str(afile))
                                        error_find.append('hombre')
                                        break
                                try:
                                    edad_int = str(edad)
                                except ValueError:
                                    if edad_int == 0:
                                        pass
                                    else:
                                        files_failed.append(str(afile))
                                        error_find.append('edad')
                                        break
                                try:
                                    edad_group_int = str(edad_group)
                                except ValueError:
                                    if edad_group_int == 0:
                                        pass
                                    else:
                                        files_failed.append(str(afile))
                                        error_find.append('edad_group')
                                        break
                                try:
                                    etnia_str = str(etnia)
                                except ValueError:
                                    if etnia_str == 0:
                                        pass
                                    else:
                                        files_failed.append(str(afile))
                                        error_find.append('etnia')
                                        break
                                try:
                                    genero_str = str(genero)
                                except ValueError:
                                    if genero_str == 0:
                                        pass
                                    else:
                                        files_failed.append(str(afile))
                                        error_find.append('genero')
                                        break
                                try:
                                    nivinst_str = str(nivinst)
                                except ValueError:
                                    if nivinst_str == 0:
                                        pass
                                    else:
                                        files_failed.append(str(afile))
                                        error_find.append('nivinst')
                                        break
                                try:
                                    anosaprob_int = str(anosaprob)
                                except ValueError:
                                    if anosaprob_int == 0:
                                        pass
                                    else:
                                        files_failed.append(str(afile))
                                        error_find.append('anosaprob')
                                        break
                                try:
                                    asisteClases_int = str(asisteClases)
                                except ValueError:
                                    if asisteClases_int == 0:
                                        pass
                                    else:
                                        files_failed.append(str(afile))
                                        error_find.append('asisteClases')
                                        break
                                try:
                                    analfabeta_int = str(analfabeta)
                                except ValueError:
                                    if analfabeta_int == 0:
                                        pass
                                    else:
                                        files_failed.append(str(afile))
                                        error_find.append('analfabeta')
                                        break
                                try:
                                    hablaEspaniol_int = str(hablaEspaniol)
                                except ValueError:
                                    if hablaEspaniol_int == 0:
                                        pass
                                    else:
                                        files_failed.append(str(afile))
                                        error_find.append('hablaEspaniol')
                                        break
                                try:
                                    hablaIndigena_int = str(hablaIndigena)
                                except ValueError:
                                    if hablaIndigena_int == 0:
                                        pass
                                    else:
                                        files_failed.append(str(afile))
                                        error_find.append('hablaIndigena')
                                        break
                                try:
                                    hablaExtranjero_int = str(hablaExtranjero)
                                except ValueError:
                                    if hablaExtranjero_int == 0:
                                        pass
                                    else:
                                        files_failed.append(str(afile))
                                        error_find.append('hablaExtranjero')
                                        break
                                try:
                                    experiencia_int = str(experiencia)
                                except ValueError:
                                    if experiencia_int == 0:
                                        pass
                                    else:
                                        files_failed.append(str(afile))
                                        error_find.append('experiencia')
                                        break
                                try:
                                    haceDeportes_int = str(haceDeportes)
                                except ValueError:
                                    if haceDeportes_int == 0:
                                        pass
                                    else:
                                        files_failed.append(str(afile))
                                        error_find.append('haceDeportes')
                                        break
                                try:
                                    horasDeportes_int = str(horasDeportes)
                                except ValueError:
                                    if horasDeportes_int == 0:
                                        pass
                                    else:
                                        files_failed.append(str(afile))
                                        error_find.append('horasDeportes')
                                        break
                                try:
                                    migracion_extranjera_int = str(migracion_extranjera)
                                except ValueError:
                                    if migracion_extranjera_int == 0:
                                        pass
                                    else:
                                        files_failed.append(str(afile))
                                        error_find.append('migracion_extranjera')
                                        break
                                try:
                                    mig_noprin_prin_int = str(mig_noprin_prin)
                                except ValueError:
                                    if mig_noprin_prin_int == 0:
                                        pass
                                    else:
                                        files_failed.append(str(afile))
                                        error_find.append('mig_noprin_prin')
                                        break
                                try:
                                    mig_prin_noprin_int = str(mig_prin_noprin)
                                except ValueError:
                                    if mig_prin_noprin_int == 0:
                                        pass
                                    else:
                                        files_failed.append(str(afile))
                                        error_find.append('mig_prin_noprin')
                                        break
                                try:
                                    mig_prin_prin_int = str(mig_prin_prin)
                                except ValueError:
                                        if mig_prin_prin_int == 0:
                                            pass
                                        else:
                                            files_failed.append(str(afile))
                                            error_find.append('mig_prin_prin')
                                            break
                                try:
                                    mig_noprin_noprin_int = str(mig_noprin_noprin)
                                except ValueError:
                                    if mig_noprin_noprin_int == 0:
                                        pass
                                    else:
                                        files_failed.append(str(afile))
                                        error_find.append('mig_noprin_noprin')
                                        break
                                try:
                                    tamano_hogar_int = str(tamano_hogar)
                                except ValueError:
                                    if tamano_hogar_int == 0:
                                        pass
                                    else:
                                        files_failed.append(str(afile))
                                        error_find.append('tamano_hogar')
                                        break
                                try:
                                    hogar_noFamiliar_int = str(hogar_noFamiliar)
                                except ValueError:
                                    if hogar_noFamiliar_int == 0:
                                        pass
                                    else:
                                        files_failed.append(str(afile))
                                        error_find.append('hogar_noFamiliar')
                                        break
                                try:
                                    part_quehaceres_int = str(part_quehaceres)
                                except ValueError:
                                    if part_quehaceres_int == 0:
                                        pass
                                    else:
                                        files_failed.append(str(afile))
                                        error_find.append('part_quehaceres')
                                        break
                                try:
                                    horas_part_quehaceres_int = str(horas_part_quehaceres)
                                except ValueError:
                                    if horas_part_quehaceres_int == 0:
                                        pass
                                    else:
                                        files_failed.append(str(afile))
                                        error_find.append('horas_part_quehaceres')
                                        break
                                try:
                                    hogar_completo_int = str(hogar_completo)
                                except ValueError:
                                    if hogar_completo_int == 0:
                                        pass
                                    else:
                                        files_failed.append(str(afile))
                                        error_find.append('hogar_completo')
                                        break
                                try:
                                    ingrl_int = str(ingrl)
                                except ValueError:
                                    if ingrl_int == 0:
                                        pass
                                    else:
                                        files_failed.append(str(afile))
                                        error_find.append('ingrl')
                                        break
                                try:
                                    ingreso_hogar_float = float(ingreso_hogar)
                                except ValueError:
                                    if ingreso_hogar_float == 0:
                                        pass
                                    else:
                                        files_failed.append(str(afile))
                                        error_find.append('ingreso_hogar')
                                        break
                                try:
                                    pobreza_int = str(pobreza)
                                except ValueError:
                                    if pobreza_int == 0:
                                        pass
                                    else:
                                        files_failed.append(str(afile))
                                        error_find.append('pobreza')
                                        break
                                try:
                                    pobreza_extrema_int = str(pobreza_extrema)
                                except ValueError:
                                    if pobreza_extrema_int == 0:
                                        pass
                                    else:
                                        files_failed.append(str(afile))
                                        error_find.append('pobreza_extrema')
                                        break
                                try:
                                    seguro_str = str(seguro)
                                except ValueError:
                                    if seguro_str == 0:
                                        pass
                                    else:
                                        files_failed.append(str(afile))
                                        error_find.append('seguro')
                                        break
                                try:
                                    pet_int = str(pet)
                                except ValueError:
                                    if pet_int == 0:
                                        pass
                                    else:
                                        files_failed.append(str(afile))
                                        error_find.append('pet')
                                        break
                                try:
                                    pei_int = str(pei)
                                except ValueError:
                                    if pei_int == 0:
                                        pass
                                    else:
                                        files_failed.append(str(afile))
                                        error_find.append('pei')
                                        break
                                try:
                                    pea_int = str(pea)
                                except ValueError:
                                    if pea_int == 0:
                                        pass
                                    else:
                                        files_failed.append(str(afile))
                                        error_find.append('pea')
                                        break
                                try:
                                    empleo_int = str(empleo)
                                except ValueError:
                                    if empleo_int == 0:
                                        pass
                                    else:
                                        files_failed.append(str(afile))
                                        error_find.append('empleo')
                                        break
                                try:
                                    desempleo_int = str(desempleo)
                                except ValueError:
                                    if desempleo_int == 0:
                                        pass
                                    else:
                                        files_failed.append(str(afile))
                                        error_find.append('desempleo')
                                        break
                                try:
                                    cesantes_int = str(cesantes)
                                except ValueError:
                                    if cesantes_int == 0:
                                        pass
                                    else:
                                        files_failed.append(str(afile))
                                        error_find.append('cesantes')
                                        break
                                try:
                                    desm_nuevo_int = str(desm_nuevo)
                                except ValueError:
                                    if desm_nuevo_int == 0:
                                        pass
                                    else:
                                        files_failed.append(str(afile))
                                        error_find.append('desm_nuevo')
                                        break
                                try:
                                    semanas_busc_trab_int = str(semanas_busc_trab)
                                except ValueError:
                                    if semanas_busc_trab_int == 0:
                                        pass
                                    else:
                                        files_failed.append(str(afile))
                                        error_find.append('semanas_busc_trab')
                                        break
                                try:
                                    desoNoBusca_int = str(desoNoBusca)
                                except ValueError:
                                    if desoNoBusca_int == 0:
                                        pass
                                    else:
                                        files_failed.append(str(afile))
                                        error_find.append('desoNoBusca')
                                        break
                                try:
                                    grupo_ocup_1_str = str(grupo_ocup_1)
                                except ValueError:
                                    if grupo_ocup_1_str == 0:
                                        pass
                                    else:
                                        files_failed.append(str(afile))
                                        error_find.append('grupo_ocup_1')
                                        break
                                try:
                                    rama_act_2_str = str(rama_act_2)
                                except ValueError:
                                    if rama_act_2_str == 0:
                                        pass
                                    else:
                                        files_failed.append(str(afile))
                                        error_find.append('rama_act_2')
                                        break
                                try:
                                    sect_informal_int = str(sect_informal)
                                except ValueError:
                                    if sect_informal_int == 0:
                                        pass
                                    else:
                                        files_failed.append(str(afile))
                                        error_find.append('sect_informal')
                                        break
                                try:
                                    sect_srvdom_int = str(sect_srvdom)
                                except ValueError:
                                    if sect_srvdom_int == 0:
                                        pass
                                    else:
                                        files_failed.append(str(afile))
                                        error_find.append('sect_srvdom')
                                        break
                                try:
                                    categ_ocupa_str = str(categ_ocupa)
                                except ValueError:
                                    if categ_ocupa_str == 0:
                                        pass
                                    else:
                                        files_failed.append(str(afile))
                                        error_find.append('categ_ocupa')
                                        break
                                try:
                                    tipo_deso_str = str(tipo_deso)
                                except ValueError:
                                    if tipo_deso_str == 0:
                                        pass
                                    else:
                                        files_failed.append(str(afile))
                                        error_find.append('tipo_deso')
                                        break
                                try:
                                    condInact_str = str(condInact)
                                except ValueError:
                                    if condInact_str == 0:
                                        pass
                                    else:
                                        files_failed.append(str(afile))
                                        error_find.append('condInact')
                                        break
                                try:
                                    rentista_int = str(rentista)
                                except ValueError:
                                    if rentista_int == 0:
                                        pass
                                    else:
                                        files_failed.append(str(afile))
                                        error_find.append('rentista')
                                        break
                                try:
                                    jubil_int = str(jubil)
                                except ValueError:
                                    if jubil_int == 0:
                                        pass
                                    else:
                                        files_failed.append(str(afile))
                                        error_find.append('jubil')
                                        break
                                try:
                                    estudiant_int = str(estudiant)
                                except ValueError:
                                    if estudiant_int == 0:
                                        pass
                                    else:
                                        files_failed.append(str(afile))
                                        error_find.append('estudiant')
                                        break
                                try:
                                    amaCasa_int = str(amaCasa)
                                except ValueError:
                                    if amaCasa_int == 0:
                                        pass
                                    else:
                                        files_failed.append(str(afile))
                                        error_find.append('amaCasa')
                                        break
                                try:
                                    incapacit_int = str(incapacit)
                                except ValueError:
                                    if incapacit_int == 0:
                                        pass
                                    else:
                                        files_failed.append(str(afile))
                                        error_find.append('incapacit')
                                        break
                                try:
                                    otro_int = str(otro)
                                except ValueError:
                                    if otro_int == 0:
                                        pass
                                    else:
                                        files_failed.append(str(afile))
                                        error_find.append('otro')
                                        break
                                try:
                                    jefeHogar_int = str(jefeHogar)
                                    if jefeHogar_int == '0' or jefeHogar == '1':
                                        files_failed.append(str(afile))
                                        error_find.append('jefeHogar')
                                        break
                                except ValueError:
                                    if jefeHogar_int == 0:
                                        pass
                                    else:
                                        files_failed.append(str(afile))
                                        error_find.append('jefeHogar')
                                        break
                                try:
                                    oplenos_int = str(oplenos)
                                except ValueError:
                                    if oplenos_int == 0:
                                        pass
                                    else:
                                        files_failed.append(str(afile))
                                        error_find.append('oplenos')
                                        break
                                try:
                                    suboc_int = str(suboc)
                                except ValueError:
                                    if suboc_int == 0:
                                        pass
                                    else:
                                        files_failed.append(str(afile))
                                        error_find.append('suboc')
                                        break
                                try:
                                    suboc1_int = str(suboc1)
                                except ValueError:
                                    if suboc1_int == 0:
                                        pass
                                    else:
                                        files_failed.append(str(afile))
                                        error_find.append('suboc1')
                                        break
                                try:
                                    condact_str = str(condact)
                                except ValueError:
                                    if condact_str == 0:
                                        pass
                                    else:
                                        files_failed.append(str(afile))
                                        error_find.append('condact')
                                        break
                                try:
                                    tipo_ocupa_str = str(tipo_ocupa)
                                except ValueError:
                                    if tipo_ocupa_str == 0:
                                        pass
                                    else:
                                        files_failed.append(str(afile))
                                        error_find.append('tipo_ocupa')
                                        break
                                try:
                                    satis_laboral_int = str(satis_laboral)
                                except ValueError:
                                    if satis_laboral_int == 0:
                                        pass
                                    else:
                                        files_failed.append(str(afile))
                                        error_find.append('satis_laboral')
                                        break
                                try:
                                    descon_bajos_ingresos_int = str(descon_bajos_ingresos)
                                except ValueError:
                                    if descon_bajos_ingresos_int == 0:
                                        pass
                                    else:
                                        files_failed.append(str(afile))
                                        error_find.append('descon_bajos_ingresos')
                                        break
                                try:
                                    descon_horarios_int = str(descon_horarios)
                                except ValueError:
                                    if descon_horarios_int == 0:
                                        pass
                                    else:
                                        files_failed.append(str(afile))
                                        error_find.append('descon_horarios')
                                        break
                                try:
                                    descon_estabil_int = str(descon_estabil)
                                except ValueError:
                                    if descon_estabil_int == 0:
                                        pass
                                    else:
                                        files_failed.append(str(afile))
                                        error_find.append('descon_estabil')
                                        break
                                try:
                                    descon_amb_laboral_int = str(descon_amb_laboral)
                                except ValueError:
                                    if descon_amb_laboral_int == 0:
                                        pass
                                    else:
                                        files_failed.append(str(afile))
                                        error_find.append('descon_amb_laboral')
                                        break
                                try:
                                    descon_activ_int = str(descon_activ)
                                except ValueError:
                                    if descon_activ_int == 0:
                                        pass
                                    else:
                                        files_failed.append(str(afile))
                                        error_find.append('descon_activ')
                                        break
                                try:
                                    sect_formal_int = str(sect_formal)
                                except ValueError:
                                    if sect_formal_int == 0:
                                        pass
                                    else:
                                        files_failed.append(str(afile))
                                        error_find.append('sect_formal')
                                        break
                                try:
                                    nocla_sector_int = str(nocla_sector)
                                except ValueError:
                                    if nocla_sector_int == 0:
                                        pass
                                    else:
                                        files_failed.append(str(afile))
                                        error_find.append('nocla_sector')
                                        break
                                try:
                                    desemab_int = str(desemab)
                                except ValueError:
                                    if desemab_int == 0:
                                        pass
                                    else:
                                        files_failed.append(str(afile))
                                        error_find.append('desemab')
                                        break
                                try:
                                    desemoc_int = str(desemoc)
                                except ValueError:
                                    if desemoc_int == 0:
                                        pass
                                    else:
                                        files_failed.append(str(afile))
                                        error_find.append('desemoc')
                                        break
                                try:
                                    suboc2_int = str(suboc2)
                                except ValueError:
                                    if suboc2_int == 0:
                                        pass
                                    else:
                                        files_failed.append(str(afile))
                                        error_find.append('suboc2')
                                        break
                                try:
                                    sub_informal_int = str(sub_informal)
                                except ValueError:
                                    if sub_informal_int == 0:
                                        pass
                                    else:
                                        files_failed.append(str(afile))
                                        error_find.append('sub_informal')
                                        break
                                try:
                                    sect_moderno_int = str(sect_moderno)
                                except ValueError:
                                    if sect_moderno_int == 0:
                                        pass
                                    else:
                                        files_failed.append(str(afile))
                                        error_find.append('sect_moderno')
                                        break
                                try:
                                    sect_agricola_int = str(sect_agricola)
                                except ValueError:
                                    if sect_agricola_int == 0:
                                        pass
                                    else:
                                        files_failed.append(str(afile))
                                        error_find.append('sect_agricola')
                                        break
                                try:
                                    sub_inv_int = str(sub_inv)
                                except ValueError:
                                    if sub_inv_int == 0:
                                        pass
                                    else:
                                        files_failed.append(str(afile))
                                        error_find.append('sub_inv')
                                        break
                                try:
                                    empleoAdecuado_int = str(empleoAdecuado)
                                except ValueError:
                                    if empleoAdecuado_int == 0:
                                        pass
                                    else:
                                        files_failed.append(str(afile))
                                        error_find.append('empleoAdecuado')
                                        break
                                try:
                                    empleoInadecuado_int = str(empleoInadecuado)
                                except ValueError:
                                    if empleoInadecuado_int == 0:
                                        pass
                                    else:
                                        files_failed.append(str(afile))
                                        error_find.append('empleoInadecuado')
                                        break
                                try:
                                    subempleo_int = str(subempleo)
                                except ValueError:
                                    if subempleo_int == 0:
                                        pass
                                    else:
                                        files_failed.append(str(afile))
                                        error_find.append('subempleo')
                                        break
                                try:
                                    subempleoXhoras_int = str(subempleoXhoras)
                                except ValueError:
                                    if subempleoXhoras_int == 0:
                                        pass
                                    else:
                                        files_failed.append(str(afile))
                                        error_find.append('subempleoXhoras')
                                        break
                                try:
                                    subempleoXingreso_int = str(subempleoXingreso)
                                except ValueError:
                                    if subempleoXingreso_int == 0:
                                        pass
                                    else:
                                        files_failed.append(str(afile))
                                        error_find.append('subempleoXingreso')
                                        break
                                try:
                                    otroEmpleoInadec_int = str(otroEmpleoInadec)
                                except ValueError:
                                    if otroEmpleoInadec_int == 0:
                                        pass
                                    else:
                                        files_failed.append(str(afile))
                                        error_find.append('otroEmpleoInadec')
                                        break
                                try:
                                    empleoNoclasificado_int = str(empleoNoclasificado)
                                except ValueError:
                                    if empleoNoclasificado_int == 0:
                                        pass
                                    else:
                                        files_failed.append(str(afile))
                                        error_find.append('empleoNoclasificado')
                                        break
                                try:
                                    empleoNoremunerado_int = str(empleoNoremunerado)
                                except ValueError:
                                    if empleoNoremunerado_int == 0:
                                        pass
                                    else:
                                        files_failed.append(str(afile))
                                        error_find.append('empleoNoremunerado')
                                        break
                                try:
                                    tipoEmpleo_str = str(tipoEmpleo)
                                except ValueError:
                                    if tipoEmpleo_str == 0:
                                        pass
                                    else:
                                        files_failed.append(str(afile))
                                        error_find.append('tipoEmpleo')
                                        break
                                try:
                                    tipoEmpleoDesag_str = str(tipoEmpleoDesag)
                                except ValueError:
                                    if tipoEmpleoDesag_str == 0:
                                        pass
                                    else:
                                        files_failed.append(str(afile))
                                        error_find.append('tipoEmpleoDesag')
                                        break
                                try:
                                    sectorEmpleo_str = str(sectorEmpleo)
                                except ValueError:
                                    if sectorEmpleo_str == 0:
                                        pass
                                    else:
                                        files_failed.append(str(afile))
                                        error_find.append('sectorEmpleo')
                                        break

                    # Borramos los archivos que tienen mal formato.
                    if len(files_failed) > 0:
                        for afile in files_failed:
                            os.remove(path_dir+str(afile))
                    if len(files_failed) == len(file_list):
                        upload_success = False
                    else:
                        #Luego se corre el load_files.sh
                        p = subprocess.Popen(['/home/patu/Downloads/ObservatorioCIEC-master/load_files',dbtable])
                        alert = p.communicate()
                        upload_success = True
                        empty = False
            else:
                empty = True
                upload_success = False
        else:
            upload_form = UploadFileForm()
            upload_success = False
    else:
        return HttpResponseRedirect('/acceso_denegado/')
    return render_to_response(template, {'upload_form': upload_form, 'upload_success':upload_success, 'empty':empty, 'files_failed':files_failed, 'error_find':error_find}, context)


def access_denied(request):
    template = 'access_denied.html'
    return render_to_response(template, context_instance=RequestContext(request, locals()))


def error_extension(request):
    template = 'error_extension.html'
    return render_to_response(template, context_instance=RequestContext(request, locals()))

def delete_data_enemdu(request):
    template = 'delete_data.html'
    return render_to_response(template, context_instance=RequestContext(request, locals()))

def eliminar_datos(request):
    template = 'delete_data.html'
    context = RequestContext(request)
    choices = request.GET['choice']
    anio = request.GET['txt_anio']
    trimestre = request.GET['txt_trimestre']
    permiso = True
    
    if anio == "" or trimestre == "":
        flag = [4]
    else:
        try:
            anio_int = int(anio)
            trimestre_int = int(trimestre)
        except ValueError:
            flag = [5]
            permiso = False
        
        if permiso:
            choices_int = int(choices)
            anio_int = int(anio)
            trimestre_int = int(trimestre)

            if choices_int == 1:
                data_ENEMDU = Data_from_2003_4
            else:
                data_ENEMDU = Data_from_2007_2

            if anio_int < 2003:
                flag = [0]
            else:
                if (trimestre_int > 0 and trimestre_int < 5):
                    procced_delete = data_ENEMDU.objects.filter(anio=anio_int).filter(trimestre=trimestre_int)
                    if (procced_delete.count() > 0):
                        procced_delete.delete()
                        flag = [1]
                    else:
                        flag = [3]
                else:
                    flag = [2]
    
    message = json.dumps(flag, cls=PythonObjectEncoder)
    return HttpResponse(message, content_type='application/json')

def eliminar_datos_rango(request):
    template = 'delete_data.html'
    context = RequestContext(request)
    choices = request.GET['choice']
    anio_1 = request.GET['txt_anio_1']
    anio_2 = request.GET['txt_anio_2']
    trimestre_1 = request.GET['txt_trimestre_1']
    trimestre_2 = request.GET['txt_trimestre_2']
    permiso = True

    if anio_1 == "" or anio_2 == "" or trimestre_1 == "" or trimestre_2 == "":
        flag = [4]
    else:
        try:
            anio_int_1 = int(anio_1)
            anio_int_2 = int(anio_2)
            trimestre_int_1 = int(trimestre_1)
            trimestre_int_2 = int(trimestre_2)
        except ValueError:
            flag = [5]
            permiso = False

        if permiso:
            choices_int = int(choices)
            anio_int_1 = int(anio_1)
            anio_int_2 = int(anio_2)
            trimestre_int_1 = int(trimestre_1)
            trimestre_int_2 = int(trimestre_2)
            
            if choices_int == 1:
                data_ENEMDU = Data_from_2003_4
            else:
                data_ENEMDU = Data_from_2007_2

            if anio_int_1 < 2003:
                flag = [1]
            elif anio_int_2 < 2003:
                flag = [2]
            elif anio_int_1 > anio_int_2:
                flag = [3]
            else:
                if (trimestre_int_1 > 0 and trimestre_int_1 < 5):
                    if (trimestre_int_2 > 0 and trimestre_int_2 < 5):
                        trim_1 = trimestre_int_1
                        trim_2 = 5
                        count = 0
                        bandera = 0
                        for i in range(anio_int_1, anio_int_2+1):
                            if i == anio_int_2:
                                trim_2 = trimestre_int_2 + 1
                            if count > 0:
                                trim_1 = 1
                            for j in range(trim_1,trim_2):
                                procced_delete = data_ENEMDU.objects.filter(anio=i).filter(trimestre=j)
                                if(procced_delete.count() > 0):
                                    procced_delete.delete()
                                else:
                                    bandera = bandera + 1
                            count = count + 1
                        if count > bandera:
                            flag = [0]
                        else:
                            flag = [6]
                    else:
                        flag = [5]
                else:
                    flag = [4]
                
    message = json.dumps(flag, cls=PythonObjectEncoder)
    return HttpResponse(message, content_type='application/json')

def eliminar_anio_rango_trim(request):
    template = 'delete_data.html'
    context = RequestContext(request)
    choices = request.GET['choice']
    txt_year = request.GET['txt_year']
    txt_tri_1 = request.GET['txt_tri_1']
    txt_tri_2 = request.GET['txt_tri_2']
    permiso = True

    if txt_year == "" or txt_tri_1 == "" or txt_tri_2 == "":
        flag = [4]
    else:
        try:
            txt_year_int = int(txt_year)
            txt_tri_1_int = int(txt_tri_1)
            txt_tri_2_int = int(txt_tri_2)
        except ValueError:
            flag = [5]
            permiso = False

        if permiso:
            choices_int = int(choices)
            txt_year_int = int(txt_year)
            txt_tri_1_int = int(txt_tri_1)
            txt_tri_2_int = int(txt_tri_2)

            if choices_int == 1:
                data_ENEMDU = Data_from_2003_4
            else:
                data_ENEMDU = Data_from_2007_2

            if txt_year_int < 2003:
                flag = [3]
            else:
                if (txt_tri_1_int > 0 and txt_tri_1_int < 5):
                    if (txt_tri_2_int > 0 and txt_tri_2_int < 5):
                        if txt_tri_2_int > txt_tri_1_int:
                            procced_delete = data_ENEMDU.objects.filter(anio=txt_year_int).filter(trimestre__range=(txt_tri_1_int,txt_tri_2_int))
                            if (procced_delete.count() > 0):
                                procced_delete.delete()
                                flag = [0]
                            else:
                                flag = [7]
                        else:
                            flag = [6]
                    else:
                        flag = [2]
                else:
                    flag = [1]
        

    message = json.dumps(flag, cls=PythonObjectEncoder)
    return HttpResponse(message, content_type='application/json')