from django.urls import path
from scheduling import schedule_appointment_views
from scheduling import clinic_schedule_views
from scheduling import clinic_holiday_views


urlpatterns = [
    path('schedule_appointments/', schedule_appointment_views.ScheduleAppointmentListCreateAPIView.as_view(), name='schedule_appointments_list_create'),
    path('schedule_appointments/<int:pk>/', schedule_appointment_views.ScheduleAppointmentRetrieveUpdateDestroyAPIView.as_view(), name='schedule_appointments_detail_view'),

    path('clinic_schedule/', clinic_schedule_views.ClinicScheduleListCreateAPIView.as_view(), name='clinic_schedule_list_create'),
    path('clinic_schedule/<int:pk>/', clinic_schedule_views.ClinicScheduleRetrieveUpdateDestroyAPIView.as_view(), name='clinic_schedule_detail_view'),

    path('clinic_holiday/', clinic_holiday_views.ClinicHolidayListCreateAPIView.as_view(), name='clinic_holiday_list_create'),
    path('clinic_holiday/<int:pk>/', clinic_holiday_views.ClinicHolidayRetrieveUpdateDestroyAPIView.as_view(), name='clinic_holiday_detail_view'),
]