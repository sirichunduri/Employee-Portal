from django.db import models
from datetime import datetime, timedelta, date
from django.utils import timezone
from django.contrib.auth.models import User
import time
import pytz


class Timesheet(models.Model):
    job = models.CharField(max_length=100)
    date = models.DateField('date')
    time = models.DateTimeField(default=timezone.now)
    employee = models.ForeignKey(User, on_delete=models.CASCADE)
    hours = models.IntegerField()

    class Meta:
        db_table = 'timesheets'
        ordering = ('-date', 'hours')

    def __unicode__(self):
        return u"%s %s - %s" % (self.person.first_name, self.person.last_name, self.date)

#
# class Name(models.Model):
#     First_name = models.CharField(max_length=100)
#     Last_name = models.CharField(max_length=100)
#     person = models.ForeignKey(User, on_delete=models.CASCADE)
#
#     class Meta:
#         db_table = 'info'
#
#     def __str__(self):
#         return self.First_name + self.Last_name
