from django.urls import path, include
from scheduling import schedule_appointment_views
from scheduling import clinic_schedule_views
from scheduling import clinic_holiday_views


# Rotas da API 
api_v1_patterns = [

    path('schedule_appointments/', schedule_appointment_views.ScheduleAppointmentListCreateAPIView.as_view(), name='schedule_appointments_list_create'),
    path('schedule_appointments/<int:pk>/', schedule_appointment_views.ScheduleAppointmentRetrieveUpdateDestroyAPIView.as_view(), name='schedule_appointments_detail_view'),

    path('clinic_schedule/', clinic_schedule_views.ClinicScheduleListCreateAPIView.as_view(), name='clinic_schedule_list_create'),
    path('clinic_schedule/<int:pk>/', clinic_schedule_views.ClinicScheduleRetrieveUpdateDestroyAPIView.as_view(), name='clinic_schedule_detail_view'),

    path('clinic_holiday/', clinic_holiday_views.ClinicHolidayListCreateAPIView.as_view(), name='clinic_holiday_list_create'),
    path('clinic_holiday/<int:pk>/', clinic_holiday_views.ClinicHolidayRetrieveUpdateDestroyAPIView.as_view(), name='clinic_holiday_detail_view'),

]

urlpatterns = [

    path('schedule_appointments/list', schedule_appointment_views.AppointmentListView.as_view(), name='schedule_appointments_list'),
    path('schedule_appointments/create/', schedule_appointment_views.AppointmentCreateView.as_view(), name='schedule_appointments_create'),
    path('schedule_appointments/update/<int:pk>/', schedule_appointment_views.AppointmentUpdateView.as_view(), name='schedule_appointments_update'),
    path('schedule_appointments/delete/<int:pk>/', schedule_appointment_views.AppointmentDeleteView.as_view(), name='schedule_appointments_delete'),
    path('schedule_appointments/detail/<int:pk>/', schedule_appointment_views.AppointmentDetailView.as_view(), name='schedule_appointments_detail'),

    path('clinic_schedule/list/', clinic_schedule_views.ClinicScheduleListView.as_view(), name='clinic_schedule_list'),
    path('clinic_schedule/create/', clinic_schedule_views.ClinicScheduleCreateView.as_view(), name='clinic_schedule_create'),
    path('clinic_schedule/update/<int:pk>/', clinic_schedule_views.ClinicScheduleUpdateView.as_view(), name='clinic_schedule_update'),
    path('clinic_schedule/delete/<int:pk>/', clinic_schedule_views.ClinicScheduleDeleteView.as_view(), name='clinic_schedule_delete'),

    path('clinic_holiday/list/', clinic_holiday_views.ClinicHolidayListView.as_view(), name='clinic_holiday_list'),
    path('clinic_holiday/create/', clinic_holiday_views.ClinicHolidayCreateView.as_view(), name='clinic_holiday_create'),
    path('clinic_holiday/update/<int:pk>/', clinic_holiday_views.ClinicHolidayUpdateView.as_view(), name='clinic_holiday_update'),
    path('clinic_holiday/delete/<int:pk>/', clinic_holiday_views.ClinicHolidayDeleteView.as_view(), name='clinic_holiday_delete'),

    path('api/v1/', include(api_v1_patterns)),
]
