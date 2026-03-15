from django.urls import path
from accounts import user_views
from accounts import patient_views
from accounts import professional_views


urlpatterns = [
    path('users/', user_views.UserListCreateApiView.as_view(), name='users_list_create'),
    path('users/<int:pk>/', user_views.UserRetrieveUpdateDestroyApiView.as_view(), name='users_detail_view'),

    path('patients/', patient_views.PatientListCreateApiView.as_view(), name='patients_list_create'),
    path('patients/<int:pk>/', patient_views.PatientRetrieveUpdateDestroyApiView.as_view(), name='patients_detail_view'),

    path('professional/', professional_views.ProfessionalListCreateApiView.as_view(), name='professional_list_create'),
    path('professional/<int:pk>/', professional_views.ProfessionalRetrieveUpdateDestroyApiView.as_view(), name='professional_detail_view'),
]
