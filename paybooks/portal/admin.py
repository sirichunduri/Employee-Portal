from django.contrib import admin
from portal.models import Timesheet


class TimesheetAdmin(admin.ModelAdmin):
	list_display = ('job', 'employee', 'date', 'hours',)
	list_filter = ('date','hours','employee',)

admin.site.register(Timesheet, TimesheetAdmin)