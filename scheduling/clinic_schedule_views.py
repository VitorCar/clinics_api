from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema_view, extend_schema
from .models import ClinicSchedule
from .forms import ClinicScheduleForm
from .serializers import ClinicScheduleSerializers, ClinicScheduleListSerializers
from app.permissions import GlobalDefaultPermissions


class ClinicScheduleListView(ListView):
    model = ClinicSchedule
    template_name = 'clinic_schedule_list.html'
    context_object_name = 'clinic_schedule' 

    def get_queryset(self):
        queryset = super().get_queryset()
        
        clinic_name = self.request.GET.get('clinic')
        day_week = self.request.GET.get('day_week')

        if clinic_name:
            queryset = queryset.filter(clinic__name__icontains=clinic_name)

        if day_week:
            queryset = queryset.filter(days_week=day_week)
            
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['week_days'] = ClinicSchedule.WeekDays.choices
        return context


class ClinicScheduleCreateView(CreateView):
    model = ClinicSchedule
    template_name = 'clinic_schedule_create.html'
    form_class = ClinicScheduleForm
    success_url = reverse_lazy('clinic_schedule_list')


class ClinicScheduleUpdateView(UpdateView):
    model = ClinicSchedule
    form_class = ClinicScheduleForm
    template_name = 'clinic_schedule_create.html' 
    success_url = reverse_lazy('clinic_schedule_list')


class ClinicScheduleDeleteView(DeleteView):
    model = ClinicSchedule
    template_name = 'clinic_schedule_delete.html'
    success_url = reverse_lazy('clinic_schedule_list')


@extend_schema_view(
    get=extend_schema(
        description='Retorna todos os agendamentos e seus dados',
        responses={200: ClinicScheduleSerializers},
        tags=['Agendamento Clínico']
    ),
    post=extend_schema(
        description='Criar um agendamento clínico',
        request=ClinicScheduleSerializers,
        responses={201: ClinicScheduleSerializers},
        tags=['Agendamento Clínico']
    )
)
class ClinicScheduleListCreateAPIView(ListCreateAPIView):

    queryset = ClinicSchedule.objects.all()
    permission_classes = (IsAuthenticated, GlobalDefaultPermissions,)
    
    def get_serializer_class(self):
        if self.request.method == "GET":
            return ClinicScheduleListSerializers
        return ClinicScheduleSerializers


@extend_schema_view(
    get=extend_schema(
        description='Retorna os dados de um agendamento clínico específico',
        responses={200: ClinicScheduleSerializers},
        tags=['Agendamento Clínico']
    ),
    put=extend_schema(
        description='Atualiza todos os dados de um agendamento clínico',
        request=ClinicScheduleSerializers,
        responses={200: ClinicScheduleSerializers},
        tags=['Agendamento Clínico']
    ),
    patch=extend_schema(
        description='Atualiza parcialmente os dados de um agendamento clínico',
        request=ClinicScheduleSerializers,
        responses={200: ClinicScheduleSerializers},
        tags=['Agendamento Clínico']
    ),
    delete=extend_schema(
        description='Remove um agendamento clínico do sistema',
        responses={204: None},
        tags=['Agendamento Clínico']
    )
)
class ClinicScheduleRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):

    queryset = ClinicSchedule.objects.all()
    permission_classes = (IsAuthenticated, GlobalDefaultPermissions,)
    serializer_class = ClinicScheduleSerializers
