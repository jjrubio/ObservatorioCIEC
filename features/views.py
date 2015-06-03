# -*- coding: utf-8 -*-
from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.template.context import RequestContext
from features.models import Description


def features(request):
	description = Description.objects.all()
	template = 'features.html'
	return render_to_response(template, context_instance = RequestContext(request,locals()))