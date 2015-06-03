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