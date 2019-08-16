from django.shortcuts import render, redirect, render_to_response
import datetime, time
from django.contrib.auth.models import User
from .models import Timesheet
from django.utils import timezone
from django.http import Http404, JsonResponse
from django.db.models import Sum
from .forms import *
from django import forms


def home(request):
    form = addName()
    return render(request, 'portal/home.html', {'form': form})


def saved_data(request):
    return render(request, 'portal/saved.html')


def report_data(request, username, year, week):
    try:
        week_begining = datetime.date(*time.strptime(year + '-0-' + week, '%Y-%w-%U')[:3])
        week_ending = week_begining + datetime.timedelta(days=7)
    except ValueError:
        raise Http404
    try:
        user = User.objects.get(username__iexact=username)
    except User.DoesNotExist:
        raise Http404

    queryset = Timesheet.objects.filter(employee=user, date__gte=week_begining, date__lt=week_ending).order_by('date',
                                                                                                               'time')
    timesheet = []
    date = week_begining
    while date <= week_ending:
        date_queryset = queryset.filter(date=date)
        timesheet += [{
            'date': date,
            'jobs': date_queryset,
            'hours': date_queryset.aggregate(Sum('hours'))['hours__sum'],
        }, ]
        date = date + datetime.timedelta(days=1)
    week_hours = queryset.aggregate(Sum('hours'))['hours__sum']

    context = {
        'week_begining': week_begining,
        'user': user,
        'week_ending': week_ending,
        'timesheet': timesheet,
        'week_hours': week_hours,

    }
    return render(request, 'portal/report_data.html', context)


def get_data(request):
    if request.method == 'POST':
        form = add_data(request.POST)
        if form.is_valid():
            a = form.save(commit=False)
            a.employee = request.user
            a.save()
            return redirect('saved')
    else:
        form = add_data()
    return render(request, 'portal/add_data.html', {'form': form})


def post_name(request):
    if request.method == 'POST':
        form = addName(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'error': False, 'data': 'Success'},)
