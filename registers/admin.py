from django.contrib import admin
from models import UserProfile
from django.contrib.auth.models import User

# Register your models here.
class AuthorAdmin(admin.ModelAdmin):
	list_display = ('__unicode__' ,'institution', 'profesion', 'contador_visita')
	
admin.site.register(UserProfile, AuthorAdmin)