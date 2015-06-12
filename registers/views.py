# -*- coding: utf-8 -*-
from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.template.context import RequestContext
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .forms import UserForm, UserProfileForm, UserFormResetPassword
from django.contrib.auth.decorators import login_required
from registers.models import UserProfile
from django.conf import settings
from django.core.mail import send_mail
import datetime, random, hashlib
from django.utils import timezone
import json
from django.core import serializers
from json import JSONEncoder
from django.contrib import messages
from models import *

class PythonObjectEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (list, dict, str, unicode, int, float, bool, type(None))):
            return JSONEncoder.default(self, obj)
        return {'_python_object': pickle.dumps(obj)}


def as_python_object(dct):
    if '_python_object' in dct:
        return pickle.loads(str(dct['_python_object']))
    return dct


def register(request):
    context = RequestContext(request)
    registered = False
    template = 'register.html'

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            first_name = user_form.cleaned_data['first_name']
            last_name = user_form.cleaned_data['last_name']
            email = user_form.cleaned_data['email']
            password_one = user_form.cleaned_data['password_one']
            password_two = user_form.cleaned_data['password_two']
            u = User.objects.create_user(username=email, password=password_one, first_name=first_name, last_name=last_name)
            u.is_active = False
            u.save()
            # Claves ramdoms
            salt = hashlib.md5(str(random.random())).hexdigest()[:5]
            activation_key = hashlib.md5(salt+email).hexdigest()
            key_expires = timezone.now() + datetime.timedelta(2)
            #profile = profile_form.save(commit=False)
            #profile.user = u
            #profile.save()
            institution = profile_form.cleaned_data['institution']
            telefono = profile_form.cleaned_data['telefono']
            direccion = profile_form.cleaned_data['direccion']
            grado_academico = profile_form.cleaned_data['grado_academico']
            profile = UserProfile.objects.create(user=u,institution=institution,telefono=telefono,direccion=direccion,grado_academico=grado_academico,activation_key=activation_key,key_expires=key_expires)
            profile.save()

            registered = True
            #Sending an confirmation mail
            email_subject = 'Subscripcion al Observatorio Economico Social de Ecuador'
            from_email = settings.EMAIL_HOST_USER
            to_list = [email]
            email_body = 'Hola, %s, y gracias por registrarte!\n\n Para activar tu cuenta haz click a este enlace:\n\nhttp://localhost:8000/confirm/%s' %(u.username,profile.activation_key)
            send_mail(email_subject,email_body,from_email,to_list,fail_silently=True)
        else:
            user_form = UserForm()
            profile_form = UserProfileForm()
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render_to_response(template, {'user_form': user_form, 'profile_form': profile_form, 'registered': registered}, context)


def user_login(request):
    context = RequestContext(request)
    template = "login.html"
    template2 = "login_error.html"

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                if user.is_superuser:
                    pass
                else:
                    login(request, user)

                    counter = UserProfile.objects.filter(user_id=user.id)
                    suma = counter[0].contador_visita
                    suma += 1
                    user_by_id = UserProfile.objects.filter(user_id=user.id).update(contador_visita = suma)

                    return HttpResponseRedirect('/definicion-indicador/')
            else:
                return HttpResponseRedirect('/acceso-denegado/')
        else:
            return HttpResponseRedirect('/error-sesion/')
    else:
        return render_to_response(template, {}, context)


# @login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')


def login_error(request):
    template = 'login_error.html'
    return render_to_response(template, context_instance = RequestContext(request,locals()))


def login_denied(request):
    template = 'access_denied.html'
    return render_to_response(template, context_instance = RequestContext(request,locals()))


def test(request):
    template = 'send_email.html'
    send_mail('Hello', 'Body goes here', settings.EMAIL_HOST_USER, ['andreacaceresm@gmail.com'], fail_silently=True)
    return render_to_response(template, context_instance = RequestContext(request,locals()))


def confirm(request,activation_key):
    if request.user.is_authenticated():
        return render_to_response('confirm.html', {'has_account': True})
    #if request.user.is_active():
        #return render_to_response('confirm.html', {'has_account_active': True})
    user_profile = UserProfile.objects.filter(activation_key=activation_key)
    user_active = User.objects.filter(username=user_profile[0].user).update(is_active=True)

    return render_to_response('confirm.html', {'success':True})


def form_reset(request):
    template = 'reset.html'
    return render_to_response(template, context_instance = RequestContext(request,locals()))


def reset_password(request):
    template = 'reset.html'
    correo = request.GET['correo']
    data_result = []

    u = User.objects.filter(username=correo)

    if not u:
        result = 2
    else:
        username = u[0].username
        user_active_key = UserProfile.objects.filter(user_id=u[0].id) #Tengo la clave de activacion
        activation_key = user_active_key[0].activation_key
        new_key_expires = timezone.now() + datetime.timedelta(1) #Se crea un nuevo tiempo de expiracion
        user_key_expires_update = UserProfile.objects.filter(user_id=u[0].id).update(key_expires=new_key_expires) #Se actualiza
        #Se manda el mail
        email_subject = 'Cambio de contrasenia'
        from_email = settings.EMAIL_HOST_USER
        to_list = [correo]
        email_body = 'Hola usuario %s, \n\n Se ha notificado que desea cambiar su contrasenia, por favor dar clic al siguiente enlace: \n\n http://localhost:8000/envio_cambio_contrasenia/%s' %(username,activation_key)
        send_mail(email_subject,email_body,from_email,to_list,fail_silently=True)
        result = 1

    data_result.append([result])
    message = json.dumps(data_result, cls=PythonObjectEncoder)
    return HttpResponse(message, content_type='application/json')


def confirm_reset_password(request,activation_key):
    template = 'form_reset_password.html'

    u = UserProfile.objects.filter(activation_key=activation_key)

    time_now = timezone.now()
    time_expire = UserProfile.objects.filter()
    time_get_database = u[0].key_expires
    
    if time_get_database < time_now:
        return HttpResponseRedirect('/cambio-expirado/')
    else:
        print 'Ok'
        user_form_reset = UserFormResetPassword()
        context = {'user_form_reset':user_form_reset}
    # user_form_reset = UserFormResetPassword()
    # context = {'user_form_reset':user_form_reset}
    # template = 'form_reset_password.html'
    return render_to_response(template, context_instance = RequestContext(request,locals()))


def form_reset_password(request):
    template = 'form_reset_password.html'
    correo = request.GET['correo']
    pass1 = request.GET['pass_1']
    pass2 = request.GET['pass_2']
    data_result = []

    u = User.objects.filter(username=correo)

    if not u:
        result = 3
    else:
        if pass1 == pass2:
            if len(pass2) < 5:
                result = 4
            else:
                u = User.objects.get(username__exact=correo)
                u.set_password(pass2)
                u.save()
                result = 1  
        else:
            result = 2
    
    data_result.append([result])
    message = json.dumps(data_result, cls=PythonObjectEncoder)
    return HttpResponse(message, content_type='application/json')


def reset_success(request):
    template = 'reset_success.html'
    return render_to_response(template, context_instance = RequestContext(request,locals()))


def reset_password_expires(request):
    template = 'reset_password_expires.html'
    return render_to_response(template, context_instance = RequestContext(request,locals()))


def is_login(request):
    template = 'indicator_calc_html'
    if request.user.is_authenticated():
            usuario = 1
    else:
            usuario = 0                 
                        
    message = json.dumps(usuario, cls=PythonObjectEncoder)
    return HttpResponse(message, content_type='application/json')