from django.urls import path, include
from clinics import clinic_views
from clinics import specialty_views
from clinics import clinic_professional_views


api_v1_patterns = [

    path('clinics/', clinic_views.ClinicListCreateAPIView.as_view(), name='clinics_list_create'),
    path('clinics/<int:pk>/', clinic_views.ClinicRetrieveUpdateDestroyAPIView.as_view(), name='clinics_detail_view'),

    path('specialty/', specialty_views.SpecialtyListCreateAPIView.as_view(), name='specialty_list_create'),
    path('specialty/<int:pk>/', specialty_views.SpecialtyRetrieveUpdateDestroyAPIView.as_view(), name='especialty_detail_view'),

    path('clinic_professionals/', clinic_professional_views.ClinicProfessionalListCreateAPIView.as_view(),                  name='clinic_professionals_list_create'),
    path('clinic-professionals/<int:pk>/', clinic_professional_views.ClinicProfessionalRetrieveUpdateDestroyAPIView.as_view(), name='clinic_professionals_detail_view'),
]


urlpatterns = [

    path('specialty/list/', specialty_views.SpecialtyListView.as_view(),name='specialty_list'),
    path('specialty/create/', specialty_views.SpecialtyCreateView.as_view(), name='specialty_create'),
    path('specialty/update/<int:pk>/', specialty_views.SpecialtyUpdateView.as_view(), name='specialty_update'),
    path('specialty/delete/<int:pk>/',  specialty_views.SpecialtyDeleteView.as_view(),name='specialty_delete'),

    path('clinics/list/', clinic_views.ClinicListView.as_view(), name='clinic_list'),
    path('clinics/create/', clinic_views.ClinicCreateView.as_view(), name='clinic_create'),
    path('clinics/update/<int:pk>/', clinic_views.ClinicUpdateView.as_view(), name='clinic_update'),
    path('clinics/delete/<int:pk>/',  clinic_views.ClinicDeleteView.as_view(), name='clinic_delete'),

    path('clinic_professionals/list', clinic_professional_views.ClinicProfessionalListView.as_view(), name='clinic_professional_list'),
    path('clinic_professionals/create/', clinic_professional_views.ClinicProfessionalCreateView.as_view(), name='clinic_professional_create'),
    path('clinic_professionals/update/<int:pk>/', clinic_professional_views.ClinicProfessionalUpdateView.as_view(), name='clinic_professional_update'),
    path('clinic_professionals/delete/<int:pk>/', clinic_professional_views.ClinicProfessionalDeleteView.as_view(), name='clinic_professional_delete'),

    path('api/v1/', include(api_v1_patterns)),
]