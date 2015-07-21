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
    path_upload_csv = '/home/patu/Desktop/oese/media/csv/'

    user = request.user
    is_super_user = user.is_superuser

    if is_super_user:

        if request.method == 'POST':
            upload_form = UploadFileForm(request.POST, request.FILES)

            if 'file' in request.FILES:
                if upload_form.is_valid():
                    file = upload_form.cleaned_data['file']
                    choices = upload_form.cleaned_data['choices']

                    if choices == '1':
                        dbtable = 'enemdu_data_from_2003_4'
                    else:
                        dbtable = 'enemdu_data_from_2007_2'

                    new_file_import = upload_csv_file(upload=request.FILES['file'])
                    new_file_import.save()
                    file_name = [ f for f in listdir(path_upload_csv) if isfile(join(path_upload_csv,f)) ]
                    var_split = file_name[0]
                    extension = var_split.split('.',1)
                    ext_val = extension[1]
                  
                    if ext_val == 'txt' or ext_val == 'csv':
                        #Luego de haber subido el archivo se corre el load_files.sh
                        p = subprocess.Popen(['/home/patu/Desktop/oese/load_files',dbtable])
                        alert = p.communicate()
                        upload_success = True
                        empty = False
                    else:
                        os.remove(path_upload_csv+file_name[0])
                        return HttpResponseRedirect('/error-extension/')
                else:
                    pass               
            else:
                empty = True
                upload_success = False
        else:
            upload_form = UploadFileForm()
            upload_success = False
    else:
        return HttpResponseRedirect('/acceso_denegado/')

    return render_to_response(template, {'upload_form': upload_form, 'upload_success':upload_success, 'empty':empty}, context)


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