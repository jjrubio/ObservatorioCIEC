from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.template.context import RequestContext
from .forms import UserCreationForms

# Create your views here.
def signup(request):
	form = UserCreationForms(request.POST or None)
	template = 'signup.html'
	if form.is_valid():
		form.save()
		return HttpResponseRedirect('/UsuarioCreado')

	return render_to_response(template, context_instance = RequestContext(request,locals()))

def signupok(request):
	template = 'ok.html'
	return render_to_response(template, context_instance = RequestContext(request,locals()))	