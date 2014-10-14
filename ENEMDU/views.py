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

def insert_data_enemdu(request):
    context = RequestContext(request)
    template = 'insert_data_enemdu.html'
    upload_success = False

    user = request.user
    is_super_user = user.is_superuser

    if is_super_user:

        if request.method == 'POST':
            upload_form = UploadFileForm(request.POST, request.FILES)

            if upload_form.is_valid():
                file = upload_form.cleaned_data['file']
                choices = upload_form.cleaned_data['choices']
                if choices == '1':
                    dbtable = 'ENEMDU_data_from_2003_4'
                else:
                    dbtable = 'ENEMDU_data_from_2007_2'
                new_file_import = upload_csv_file(upload=request.FILES['file'])
                new_file_import.save()
                #Luego de haber subido el archivo se corre el load_files.sh
                #subprocess.call('/home/patu/Downloads/ObservatorioCIEC-master/load_files.sh')
                #subprocess.call('/home/patu/Downloads/ObservatorioCIEC-master/load_files')
                subprocess.Popen(['/home/jaruban/ObservatorioCIEC/load_files',dbtable])
                upload_success = True
            else:
                upload_form = UploadFileForm()
                upload_success = False
        else:
            upload_form = UploadFileForm()
            upload_success = False
    else:
        return HttpResponseRedirect('/acceso_denegado/')

    return render_to_response(template, {'upload_form': upload_form, 'upload_success':upload_success}, context)

def access_denied(request):
    template = 'access_denied.html'
    return render_to_response(template, context_instance=RequestContext(request, locals()))