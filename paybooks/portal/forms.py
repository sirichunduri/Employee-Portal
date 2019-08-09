from django import forms
from .models import Timesheet
from django.contrib.auth.models import User

class add_data(forms.ModelForm):
	date = forms.DateField()
	job = forms.CharField(max_length=100)
	hours = forms.IntegerField()
	class Meta:
		model = Timesheet
		fields = ['date','job','hours']