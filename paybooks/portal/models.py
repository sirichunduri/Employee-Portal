from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Timesheet(models.Model):
    job = models.CharField(max_length=100)
    date = models.DateField()
    time = models.DateTimeField(default=timezone.now)
    employee = models.ForeignKey(User, on_delete=models.CASCADE)
    hours = models.IntegerField()

    class Meta:
        db_table = 'timesheets'
        ordering = ('-date', 'hours')

    def __unicode__(self):
        return u"%s %s - %s" % (self.person.first_name, self.person.last_name, self.date)

class JobTitle(models.Model):
    Title = models.CharField(max_length=100)