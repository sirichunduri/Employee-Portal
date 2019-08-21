from django.shortcuts import render, redirect, render_to_response
import time
from django.contrib.auth.models import User
from django.http import Http404, JsonResponse, HttpResponse
from .forms import *
from .models import *

def home(request):
    return render(request, 'portal/home.html')


def report_data(request):
    user = request.user
    if request.method == 'POST':
        form = reportData(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            try:
                week_begining = datetime.date(
                    *time.strptime(str(data['year']) + '-0-' + str(data['week']), '%Y-%w-%U')[:3])
                week_ending = week_begining + datetime.timedelta(days=7)
            except ValueError:
                raise Http404
            queryset = Timesheet.objects.filter(employee=user, date__gte=week_begining, date__lt=week_ending).order_by(
                'date',
                'time')
            timesheet = []
            week_hours = 0
            date = week_begining
            while date <= week_ending:
                date_queryset = queryset.filter(date=date)
                for i in date_queryset:
                    timesheet += [{
                        'date': date,
                        'jobs': i.job,
                        'hours': i.hours,
                    }, ]
                    week_hours += i.hours
                date = date + datetime.timedelta(days=1)
            context = {
                'week_begining': week_begining,
                'week_ending': week_ending,
                'week_hours': week_hours
            }
            return JsonResponse({'error': False, 'context': context, 'timesheet': timesheet})

    else:
        form = reportData()
    return render(request, 'portal/report_data.html', {'form': form})


def get_data(request):
    if request.method == 'POST':
        form = add_data(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            get_user = User.objects.get(username=request.user)
            try:
                user_data = Timesheet.objects.get(employee_id=get_user, date=data['date'])
                if user_data:
                    user_data.job = data['job']
                    user_data.hours = data['hours']
                    user_data.save()
            except:
                a = Timesheet(**data)
                a.employee = request.user
                a.save()
            return JsonResponse({'error': False, 'data': 'Data Inserted!!'}, )
    else:
        form = add_data()
    return render(request, 'portal/add_data.html', {'form': form})


def post_name(request):
    user_obj = User.objects.get(id=request.user.id)
    first_name = user_obj.first_name
    last_name = user_obj.last_name
    if first_name and last_name:
        name = first_name + ' ' + last_name
    else:
        name = request.user

    if request.method == 'POST':
        form = addName(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            name_obj = User.objects.get(id=request.user.id)
            name_obj.first_name = data['First_name']
            name_obj.last_name = data['Last_name']
            name_obj.save()
            name = data['First_name'] + ' ' + data['Last_name']
            return JsonResponse({'error': False, 'name': name}, )
    else:
        form = addName()
        return render(request, 'portal/full_name.html', {'form': form, 'name': name})


def jobtitle(request):
    if request.user.is_superuser:
        if request.method == 'POST':
            form = jobTitle(request.POST)
            if form.is_valid():
                data = form.cleaned_data
                obj = JobTitle(**data)
                obj.save()
                return JsonResponse({'error': False, 'data': "Title inserted"}, )
        else:
            form = jobTitle()
            return render(request, 'portal/jobtitle.html', {'form': form})
    else:
        return HttpResponse('401 Unauthorized', status=401)
