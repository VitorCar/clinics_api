from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from django.db.models import Q
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema_view, extend_schema
from .models import ScheduleAppointment
from .forms import ScheduleAppointmentForm
from .serializers import ScheduleAppointmentSerializers, ScheduleAppointmentListSerializers
from accounts.utils import is_professional, is_patient
from app.permissions import GlobalDefaultPermissions, IsOwnerOrClinic


class AppointmentListView(ListView):
    model = ScheduleAppointment
    template_name = 'appointment_list.html'
    context_object_name = 'appointments'

    def get_queryset(self):
        queryset = super().get_queryset().select_related(
            'patient__user', 
            'professional__user', 
            'clinic'
        ).order_by('-scheduled_date', '-scheduled_time')
        
        q = self.request.GET.get('q')
        date_filter = self.request.GET.get('date')
        status_filter = self.request.GET.get('status')

        if q:
            queryset = queryset.filter(
                Q(patient__user__full_name__icontains=q) | 
                Q(professional__user__full_name__icontains=q)
            )
            
        if date_filter:
            queryset = queryset.filter(scheduled_date=date_filter)
            
        if status_filter:
            queryset = queryset.filter(status=status_filter)
            
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['status_choices'] = ScheduleAppointment.Status.choices
        return context


class AppointmentCreateView(CreateView):
    model = ScheduleAppointment
    form_class = ScheduleAppointmentForm
    template_name = 'appointment_create.html'
    success_url = reverse_lazy('schedule_appointments_list')


class AppointmentUpdateView(UpdateView):
    model = ScheduleAppointment
    form_class = ScheduleAppointmentForm
    template_name = 'appointment_create.html'
    success_url = reverse_lazy('schedule_appointments_list')


class AppointmentDetailView(DetailView):
    model = ScheduleAppointment
    template_name = 'appointment_detail.html'
    context_object_name = 'appointment'

    def get_queryset(self):
        return super().get_queryset().select_related(
            'patient__user', 
            'professional__user', 
            'clinic'
        )


class AppointmentDeleteView(DeleteView):
    model = ScheduleAppointment
    template_name = 'appointment_delete.html'
    success_url = reverse_lazy('schedule_appointments_list')


@extend_schema_view(
    get=extend_schema(
        description='Retorna todos os agendamentos e seus dados',
        responses={200: ScheduleAppointmentSerializers},
        tags=['Agendar_Consultas']
    ),
    post=extend_schema(
        description='Criar um agendamento de consulta',
        request=ScheduleAppointmentSerializers,
        responses={201: ScheduleAppointmentSerializers},
        tags=['Agendar_Consultas']
    )
)
class ScheduleAppointmentListCreateAPIView(ListCreateAPIView):

    permission_classes = (IsAuthenticated, GlobalDefaultPermissions,)

    def get_queryset(self):

        user = self.request.user

        queryset = ScheduleAppointment.objects.select_related(
            "professional__user",
            "patient__user",
            "clinic"
        )

        # PROFISSIONAL
        if is_professional(user):
            return queryset.filter(
                professional=user.professional
            )

        # PACIENTE
        if is_patient(user):
            return queryset.filter(
                patient=user.patient
            )

        # CLÍNICA / ADMIN
        if user.is_staff:
            return queryset

        return ScheduleAppointment.objects.none()
    
    def get_serializer_class(self):
        if self.request.method == "GET":
            return ScheduleAppointmentListSerializers
        return ScheduleAppointmentSerializers


@extend_schema_view(
    get=extend_schema(
        description='Retorna os dados de um agendamento específico',
        responses={200: ScheduleAppointmentSerializers},
        tags=['Agendar_Consultas']
    ),
    put=extend_schema(
        description='Atualiza todos os dados de um agendamento',
        request=ScheduleAppointmentSerializers,
        responses={200: ScheduleAppointmentSerializers},
        tags=['Agendar_Consultas']
    ),
    patch=extend_schema(
        description='Atualiza parcialmente os dados de um agendamento',
        request=ScheduleAppointmentSerializers,
        responses={200: ScheduleAppointmentSerializers},
        tags=['Agendar_Consultas']
    ),
    delete=extend_schema(
        description='Remove um agendamento do sistema',
        responses={204: None},
        tags=['Agendar_Consultas']
    )
)
class ScheduleAppointmentRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):

    queryset = ScheduleAppointment.objects.all()
    permission_classes = (IsAuthenticated, GlobalDefaultPermissions, IsOwnerOrClinic,)
    
    def get_serializer_class(self):
        if self.request.method == "GET":
            return ScheduleAppointmentListSerializers
        return ScheduleAppointmentSerializers
