from django.urls import path
from consultations import consultations_views
from consultations import prescriptions_views


urlpatterns = [
    path('consultations/', consultations_views.ConsultationListCreateAPIView.as_view(), name='consultations_list_create'),
    path('consultations/<int:pk>/', consultations_views.ConsultationRetrieveUpdateDestroyAPIView.as_view(), name='consultations_detail_view'),

    path('prescriptions/', prescriptions_views.PrescriptionListCreateAPIView.as_view(), name='prescriptions_list_create'),
    path('prescriptions/<int:pk>/', prescriptions_views.PrescriptionRetrieveUpdateDestroyAPIView.as_view(), name='prescriptions_detail_view'),
]
