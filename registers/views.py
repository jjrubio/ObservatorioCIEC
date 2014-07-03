from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.template.context import RequestContext
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .forms import UserForm, UserProfileForm
from django.contrib.auth.decorators import login_required
from registers.models import UserProfile

# Create your views here.
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
			u.save()

			profile = profile_form.save(commit=False)
			profile.user = u
			profile.save()

			registered = True
		else:
			print user_form.errors, profile_form.errors

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
				login(request, user)

				counter = UserProfile.objects.filter(user_id=user.id)
				suma = counter[0].contador_visita
				suma += 1
				user_by_id = UserProfile.objects.filter(user_id=user.id).update(contador_visita = suma)

				return HttpResponseRedirect('/definicion-indicador/')
			else:
				#return HttpResponse("Cuenta deshabilitada, por favor comuniquese con...")
				return HttpResponseRedirect('/access_denied/')
		else:
			print "Credenciales no validas: {0} {1}".format(username,password)
			#return HttpResponse("Credenciales invalidas")
			return HttpResponseRedirect('/error_login/')
	else:
		return render_to_response(template, {}, context)

@login_required
def user_logout(request):
	logout(request)
	return HttpResponseRedirect('/')

def login_error(request):
	template = 'login_error.html'
	return render_to_response(template, context_instance = RequestContext(request,locals()))

def login_denied(request):
	template = 'access_denied.html'
	return render_to_response(template, context_instance = RequestContext(request,locals()))