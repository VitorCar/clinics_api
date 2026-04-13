from django.urls import path, include
from .views import GetMedicinesFixedView, ExternalMedicineListView


api_v1_patterns = [
    path('medicines/', GetMedicinesFixedView.as_view(), name='medicines_list')
]


urlpatterns = [
    path('medicines_api/', ExternalMedicineListView.as_view(), name='medicine_external_list'),

    path('api/v1/', include(api_v1_patterns)),
]