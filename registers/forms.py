from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class UserCreationForms(UserCreationForm):
	email = forms.EmailField()

	class Meta:
		model = User
		fields = ('username', 'email')

class UserAuthenticationForm(forms.Form):
	username = forms.CharField(label='UserName')
	password = forms.CharField(label='Password', widget=forms.PasswordInput)
	
	def __init__(self, *args, **kwargs)	:
		self.user_cache = None
		super(UserAuthenticationForm, self).__init__(*args, **kwargs)

	def clean(self):
		username = self.cleaned_data.get('username')
		password = self.cleaned_data.get('password')

		self.user_cache = authenticate(username=username, password=password)

		if self.user_cache is None:
			raise forms.ValidationError('Usuario Incorrecto')
		elif not self.user_cache.is_active:
			raise forms.ValidationError('Usuario Inactivo')

		return self.cleaned_data

	def get_user(self):
		return self.user_cache

