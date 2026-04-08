from django.urls import path, include
from consultations import consultations_views
from consultations import prescriptions_views


api_v1_patterns = [

    path('consultations/', consultations_views.ConsultationListCreateAPIView.as_view(), name='consultations_list_create'),
    path('consultations/<int:pk>/', consultations_views.ConsultationRetrieveUpdateDestroyAPIView.as_view(), name='consultations_detail_view'),

    path('prescriptions/', prescriptions_views.PrescriptionListCreateAPIView.as_view(), name='prescriptions_list_create'),
    path('prescriptions/<int:pk>/', prescriptions_views.PrescriptionRetrieveUpdateDestroyAPIView.as_view(), name='prescriptions_detail_view'),
]


urlpatterns = [

    path('consultations/list/', consultations_views.ConsultationListView.as_view(),name='consultation_list'),
    path('consultations/create/', consultations_views.ConsultationCreateView.as_view(), name='consultation_create'),
    path('consultations/update/<int:pk>/', consultations_views.ConsultationUpdateView.as_view(), name='consultation_update'),
    path('consultations/delete/<int:pk>/', consultations_views.ConsultationDeleteView.as_view(),name='consultation_delete'),
    path('consultations/detail/<int:pk>/', consultations_views.ConsultationDetailView.as_view(), name='consultation_detail'),

    path('prescriptions/list/', prescriptions_views.PrescriptionListView.as_view(),name='prescription_list'),
    path('prescriptions/create/', prescriptions_views.PrescriptionCreateView.as_view(), name='prescription_create'),
    path('prescriptions/update/<int:pk>/', prescriptions_views.PrescriptionUpdateView.as_view(), name='prescription_update'),
    path('prescriptions/delete/<int:pk>/', prescriptions_views.PrescriptionDeleteView.as_view(),name='prescription_delete'),
    path('prescriptions/detail/<int:pk>/', prescriptions_views.PrescriptionDetailView.as_view(), name='prescription_detail'),

    path('api/v1/', include(api_v1_patterns)),
]
