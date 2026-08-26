from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from django.db.models import Q
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema_view, extend_schema
from .models import ScheduleAppointment
from .forms import ScheduleAppointmentForm
from .serializers import ScheduleAppointmentSerializers, ScheduleAppointmentListSerializers
from accounts.utils import is_professional, is_patient, is_admin
from app.permissions import GlobalDefaultPermissions, IsOwnerOrClinic


class AppointmentListView(LoginRequiredMixin, ListView):
    model = ScheduleAppointment
    template_name = 'appointment_list.html'
    context_object_name = 'appointments'
    paginate_by = 10

    def get_queryset(self):
        user = self.request.user
        queryset = super().get_queryset().select_related(
            'patient__user',
            'professional__user',
            'clinic'
        ).order_by('-scheduled_date', '-scheduled_time')

        # 1. Administrador/Staff: acesso total (com filtros opcionais de busca)
        if is_admin(user):
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

        # 2. Paciente: só vê os próprios agendamentos
        if is_patient(user):
            return queryset.filter(patient=user.patient)

        # 3. Profissional: só vê os agendamentos marcados com ele
        if is_professional(user):
            return queryset.filter(professional=user.professional)

        # Qualquer outro papel autenticado: não vê nada
        return queryset.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['status_choices'] = ScheduleAppointment.Status.choices
        context['can_create'] = is_admin(user := self.request.user) or is_professional(user) or is_patient(user)
        context['can_edit'] = context['can_create']
        context['can_delete'] = is_admin(self.request.user)
        return context


class AppointmentCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = ScheduleAppointment
    form_class = ScheduleAppointmentForm
    template_name = 'appointment_create.html'
    success_url = reverse_lazy('schedule_appointments_list')

    def test_func(self):
        user = self.request.user
        return is_admin(user) or is_professional(user) or is_patient(user)


class AppointmentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = ScheduleAppointment
    form_class = ScheduleAppointmentForm
    template_name = 'appointment_create.html'
    success_url = reverse_lazy('schedule_appointments_list')

    def test_func(self):
        user = self.request.user
        if is_admin(user):
            return True
        appt = self.get_object()
        if is_patient(user):
            return appt.patient == user.patient
        if is_professional(user):
            return appt.professional == user.professional
        return False

    def get_queryset(self):
        user = self.request.user
        if is_admin(user):
            return ScheduleAppointment.objects.all()
        if is_patient(user):
            return ScheduleAppointment.objects.filter(patient=user.patient)
        if is_professional(user):
            return ScheduleAppointment.objects.filter(professional=user.professional)
        return ScheduleAppointment.objects.none()


class AppointmentDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = ScheduleAppointment
    template_name = 'appointment_detail.html'
    context_object_name = 'appointment'

    def get_queryset(self):
        return super().get_queryset().select_related(
            'patient__user',
            'professional__user',
            'clinic'
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        appt = self.object
        context['can_edit'] = (
            is_admin(user)
            or (is_patient(user) and appt and appt.patient == user.patient)
            or (is_professional(user) and appt and appt.professional == user.professional)
        )
        context['can_delete'] = is_admin(user) or (
            is_professional(user) and appt and appt.professional == user.professional
        )
        return context

    def test_func(self):
        appointment = self.get_object()
        user = self.request.user

        # 1. Se for Administrador/Staff, tem acesso total
        if is_admin(user):
            return True

        # 2. Se for Paciente, só acessa se o agendamento for DELE
        if is_patient(user):
            return appointment.patient == user.patient

        # 3. Se for Profissional, só acessa se a consulta for COM ELE
        if is_professional(user):
            return appointment.professional == user.professional
        return False


class AppointmentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = ScheduleAppointment
    template_name = 'appointment_delete.html'
    success_url = reverse_lazy('schedule_appointments_list')

    def test_func(self):
        user = self.request.user
        if is_admin(user):
            return True
        if is_professional(user):
            return self.get_object().professional == user.professional
        return False

    def get_queryset(self):
        user = self.request.user
        if is_admin(user):
            return ScheduleAppointment.objects.all()
        if is_professional(user):
            return ScheduleAppointment.objects.filter(professional=user.professional)
        return ScheduleAppointment.objects.none()


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
        if is_admin(user):
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
