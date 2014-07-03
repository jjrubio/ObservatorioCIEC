from django import forms
from django.contrib.auth.models import User
from registers.models import UserProfile

class UserForm(forms.Form):
	first_name = forms.CharField(label="Nombre", widget=forms.TextInput(), required=True)
	last_name = forms.CharField(label="Apellido", widget=forms.TextInput(), required=True)
	email = forms.EmailField(label="Correo Electronico", widget=forms.TextInput(), required=True)
	password_one = forms.CharField(label="Password", widget=forms.PasswordInput(render_value=False))
	password_two = forms.CharField(label="Confirmar password", widget=forms.PasswordInput(render_value=False))

	def clean_email(self):
		email = self.cleaned_data['email']
		try:
			u = User.objects.get(username=email)
		except User.DoesNotExist:
			return email
		raise forms.ValidationError('Correo Electronico ya registrado')

	def clean_password_two(self):
		password_one = self.cleaned_data['password_one']
		password_two = self.cleaned_data['password_two']
		if password_one == password_two:
			pass
		else:
			raise forms.ValidationError('Password no coinciden')


class UserProfileForm(forms.ModelForm):
	class Meta:
		model = UserProfile
		fields = ('institution', 'telefono', 'direccion', 'grado_academico',)