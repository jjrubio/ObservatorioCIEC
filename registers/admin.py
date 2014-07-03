from django.contrib import admin
from models import UserProfile
from django.contrib.auth.models import User

# Register your models here.
class AuthorAdmin(admin.ModelAdmin):
	list_display = ('grado_academico' ,'__unicode__' ,'institution', 'telefono' , 'direccion' ,'contador_visita',)

admin.site.register(UserProfile, AuthorAdmin)