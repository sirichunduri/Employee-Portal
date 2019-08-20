from django import forms
from .models import Timesheet
import datetime

class add_data(forms.ModelForm):
    date = forms.DateField()
    job = forms.CharField(max_length=100)
    hours = forms.IntegerField()

    class Meta:
        model = Timesheet
        fields = ['date', 'job', 'hours']


class addName(forms.Form):
    First_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    Last_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))

class reportData(forms.Form):
    year = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}), min_value=2000, max_value=datetime.date.today().year)
    week = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}), min_value=1, max_value=52)