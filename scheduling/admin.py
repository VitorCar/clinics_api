from django.contrib import admin
from scheduling.models import ScheduleAppointment, ClinicSchedule, ClinicHoliday


@admin.register(ScheduleAppointment)
class ScheduleAppointmentAdmin(admin.ModelAdmin):

    list_display = ('id', 'scheduled_date', 'scheduled_time', 'status', 'reason_for_consultation', 'average_duration', 'created_at', 'updated_at')
    search_fields = ('id', 'status',)


@admin.register(ClinicSchedule)
class ClinicScheduleAdmin(admin.ModelAdmin):

    list_display = ('id', 'days_week', 'open_time', 'close_time', 'is_open', 'created_at', 'updated_at')
    search_fields = ('id',)


@admin.register(ClinicHoliday)
class ClinicHolidayAdmin(admin.ModelAdmin):

    list_display = ('id', 'date', 'description', 'created_at', 'updated_at')
    search_fields = ('id',)
