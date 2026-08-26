from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema_view, extend_schema
from .models import ClinicSchedule
from .forms import ClinicScheduleForm
from .serializers import ClinicScheduleSerializers, ClinicScheduleListSerializers
from app.permissions import GlobalDefaultPermissions
from accounts.utils import is_admin


class ClinicScheduleListView(LoginRequiredMixin, ListView):
    model = ClinicSchedule
    template_name = 'clinic_schedule_list.html'
    context_object_name = 'clinic_schedule'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset().select_related('clinic')

        # ADMIN: permite filtros de busca
        if is_admin(self.request.user):
            clinic_name = self.request.GET.get('clinic')
            day_week = self.request.GET.get('day_week')
            if clinic_name:
                queryset = queryset.filter(clinic__name__icontains=clinic_name)
            if day_week:
                queryset = queryset.filter(days_week=day_week)
            return queryset

        # PACIENTE/PROFISSIONAL: vê todos os horários das clínicas
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['week_days'] = ClinicSchedule.WeekDays.choices
        context['can_manage'] = is_admin(self.request.user)
        return context


class ClinicScheduleCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = ClinicSchedule
    template_name = 'clinic_schedule_create.html'
    form_class = ClinicScheduleForm
    success_url = reverse_lazy('clinic_schedule_list')

    def test_func(self):
        return is_admin(self.request.user)


class ClinicScheduleUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = ClinicSchedule
    form_class = ClinicScheduleForm
    template_name = 'clinic_schedule_create.html'
    success_url = reverse_lazy('clinic_schedule_list')

    def test_func(self):
        return is_admin(self.request.user)


class ClinicScheduleDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = ClinicSchedule
    template_name = 'clinic_schedule_delete.html'
    success_url = reverse_lazy('clinic_schedule_list')

    def test_func(self):
        return is_admin(self.request.user)


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