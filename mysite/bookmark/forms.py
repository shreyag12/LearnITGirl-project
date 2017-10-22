import re
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
import datetime #for checking renewal date range.
from django import forms

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
	
class signUpForm(forms.Form):
	email = forms.EmailField(widget=forms.TextInput,required = True,max_length = 30,label = 'Email')
	password=forms.CharField(label = 'Password',widget=forms.PasswordInput,required = True, max_length = 30)
	password2=forms.CharField(label = 'Confirm password',widget=forms.PasswordInput,required = 'true',max_length = 30)

	def clean_username(self):
		try:
			user = User.objects.get(username__iexact=self.cleaned_data['username'])
		except User.DoesNotExist:
			return self.cleaned_data['username']
		raise forms.ValidationError(("The username already exists. Please try another one"))
	def clean_password(self):
		if 'password' in self.cleaned_data and 'password2' in self.cleaned_data:
			if self.cleaned_data['password'] != self.cleaned_data['password2']:
				raise forms.ValidationError(_("The two password fields did not match."))
		return self.cleaned_data