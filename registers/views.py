from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.template.context import RequestContext
from django.contrib.auth import authenticate, login, logout
from .forms import UserForm, UserProfileForm
from django.contrib.auth.decorators import login_required

# Create your views here.
def register(request):
	context = RequestContext(request)
	registered = False
	template = 'register.html'

	if request.method == 'POST':
		user_form = UserForm(data=request.POST)
		profile_form = UserProfileForm(data=request.POST)

		if user_form.is_valid() and profile_form.is_valid():
			user = user_form.save()
			user.set_password(user.password)
			user.save()

			profile = profile_form.save(commit=False)
			profile.user = user
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

	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']

		user = authenticate(username=username, password=password)
		if user:
			if user.is_active:
				login(request, user)
				return HttpResponseRedirect('/lista-indicadores/')
			else:
				return HttpResponse("Cuenta deshabilitada, por favor comuniquese con...")
		else:
			print "Credenciales no validas: {0} {1}".format(username,password)
			return HttpResponse("Credenciales invalidas")
	else:
		return render_to_response(template, {}, context)

@login_required
def user_logout(request):
	logout(request)
	return HttpResponseRedirect('/')