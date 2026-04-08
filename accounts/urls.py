from django.urls import path, include
from accounts import user_views
from accounts import patient_views
from accounts import professional_views
from accounts import stats_view


api_v1_patterns = [

    path('users/', user_views.UserListCreateApiView.as_view(), name='users_list_create'),
    path('users/<int:pk>/', user_views.UserRetrieveUpdateDestroyApiView.as_view(), name='users_detail_view'),

    path('patients/', patient_views.PatientListCreateApiView.as_view(), name='patients_list_create'),
    path('patients/<int:pk>/', patient_views.PatientRetrieveUpdateDestroyApiView.as_view(), name='patients_detail_view'),

    path('professional/', professional_views.ProfessionalListCreateApiView.as_view(), name='professional_list_create'),
    path('professional/<int:pk>/', professional_views.ProfessionalRetrieveUpdateDestroyApiView.as_view(), name='professional_detail_view'),

    path('stats/', stats_view.StatsView.as_view(), name='stats'),
]

urlpatterns = [

    path('user/list/', user_views.UserListView.as_view(), name='user_list'),
    path('user/create/', user_views.UserCreateView.as_view(), name='user_create'),
    path('user/update/<int:pk>/', user_views.UserUpdateView.as_view(), name='user_update'),
    path('user/password/<int:pk>/', user_views.UserPasswordView.as_view(), name='user_password'),
    path('user/delete/<int:pk>/', user_views.UserDeleteView.as_view(), name='user_delete'),

    path('patients/list/', patient_views.PatientListView.as_view(), name='patient_list'),
    path('patients/create/', patient_views.PatientCreateView.as_view(), name='patient_create'),
    path('patients/update/<int:pk>/', patient_views.PatientUpdateView.as_view(), name='patient_update'),
    path('patients/delete/<int:pk>/', patient_views.PatientDeleteView.as_view() ,name='patient_delete'),

    path('professional/list/', professional_views.ProfessionalListView.as_view(), name='professional_list'),
    path('professional/create/', professional_views.ProfessionalCreateView.as_view(), name='professional_create'),
    path('professional/update/<int:pk>/', professional_views.ProfessionalUpdateView.as_view(), name='professional_update'),
    path('professional/delete/<int:pk>/', professional_views.ProfessionalDeleteView.as_view(),name='professional_delete'),

    path('api/v1/', include(api_v1_patterns)),
]
