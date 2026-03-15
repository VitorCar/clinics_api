from django.urls import path
from clinics import clinic_views
from clinics import specialty_views
from clinics import clinic_professional_views


urlpatterns = [
    path('clinics/', clinic_views.ClinicListCreateAPIView.as_view(), name='clinics_list_create'),
    path('clinics/<int:pk>/', clinic_views.ClinicRetrieveUpdateDestroyAPIView.as_view(), name='clinics_detail_view'),

    path('specialty/', specialty_views.SpecialtyListCreateAPIView.as_view(), name='specialty_list_create'),
    path('specialty/<int:pk>/', specialty_views.SpecialtyRetrieveUpdateDestroyAPIView.as_view(), name='especialty_detail_view'),

    path('clinic_professionals/', clinic_professional_views.ClinicProfessionalListCreateAPIView.as_view(),                  name='clinic_professionals_list_create'),
    path('clinic-professionals/<int:pk>/', clinic_professional_views.ClinicProfessionalRetrieveUpdateDestroyAPIView.as_view(), name='clinic_professionals_detail_view'),
]