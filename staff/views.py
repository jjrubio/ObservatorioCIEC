# -*- coding: utf-8 -*-
from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.template.context import RequestContext
from staff.models import Personal_data


def team_group(request):
	profile = Personal_data.objects.all()
	template = 'team.html'
	return render_to_response(template, context_instance = RequestContext(request,locals()))