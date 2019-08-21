from django import forms
from .models import *
import datetime


class add_data(forms.Form):
    date = forms.DateField(widget=forms.DateInput())
    job_choice = [('', 'Select JobTitle')]+[(i['Title'], i['Title']) for i in JobTitle.objects.values('Title').distinct()]
    job = forms.ChoiceField(choices=job_choice, widget=forms.Select(attrs={'class':'form-control'}))
    #job = forms.ModelChoiceField(queryset=JobTitle.objects.values_list("Title", flat=True), empty_label="Select JobTitle", widget=forms.Select(attrs={'class':'form-control'}))
    hours = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}))

class addName(forms.Form):
    First_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    Last_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))


class reportData(forms.Form):
    year = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}), min_value=2000,
                              max_value=datetime.date.today().year)
    week = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}), min_value=1, max_value=52)


class jobTitle(forms.Form):
    Title = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
