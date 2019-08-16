from django import forms
from .models import Timesheet,Name
from django.contrib.auth.models import User


class add_data(forms.ModelForm):
    date = forms.DateField()
    job = forms.CharField(max_length=100)
    hours = forms.IntegerField()

    class Meta:
        model = Timesheet
        fields = ['date', 'job', 'hours']


class addName(forms.ModelForm):
    First_name = forms.CharField(max_length=100)
    Last_name = forms.CharField(max_length=100)

    class Meta:
        model = Name
        fields = ['First_name', 'Last_name']
