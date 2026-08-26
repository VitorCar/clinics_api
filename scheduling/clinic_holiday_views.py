from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema_view, extend_schema
from .forms import ClinicHolidayForm
from .models import ClinicHoliday
from .serializers import ClinicHolidaySerializers, ClinicHolidayListSerializer
from app.permissions import GlobalDefaultPermissions
from accounts.utils import is_admin


class ClinicHolidayListView(LoginRequiredMixin, ListView):
    model = ClinicHoliday
    template_name = 'clinic_holiday_list.html'
    context_object_name = 'clinic_holidays'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset().select_related('clinic').order_by('date')

        # ADMIN: permite filtros de busca
        if is_admin(self.request.user):
            clinic_name = self.request.GET.get('clinic')
            date_filter = self.request.GET.get('date')
            if clinic_name:
                queryset = queryset.filter(clinic__name__icontains=clinic_name)
            if date_filter:
                queryset = queryset.filter(date=date_filter)
            return queryset

        # PACIENTE/PROFISSIONAL: vê todos os feriados/recessos
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['can_manage'] = is_admin(self.request.user)
        return context


class ClinicHolidayCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = ClinicHoliday
    form_class = ClinicHolidayForm
    template_name = 'clinic_holiday_create.html'
    success_url = reverse_lazy('clinic_holiday_list')

    def test_func(self):
        return is_admin(self.request.user)


class ClinicHolidayUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = ClinicHoliday
    form_class = ClinicHolidayForm
    template_name = 'clinic_holiday_create.html'
    success_url = reverse_lazy('clinic_holiday_list')

    def test_func(self):
        return is_admin(self.request.user)


class ClinicHolidayDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = ClinicHoliday
    template_name = 'clinic_holiday_delete.html'
    success_url = reverse_lazy('clinic_holiday_list')

    def test_func(self):
        return is_admin(self.request.user)


@extend_schema_view(
    get=extend_schema(
        description='Retorna todas as férias clínicas e seus dados',
        responses={200: ClinicHolidaySerializers},
        tags=['Férias Clínica']
    ),
    post=extend_schema(
        description='Criar uma férias clínica',
        request=ClinicHolidaySerializers,
        responses={201: ClinicHolidaySerializers},
        tags=['Férias Clínica']
    )
)
class ClinicHolidayListCreateAPIView(ListCreateAPIView):

    queryset = ClinicHoliday.objects.all()
    permission_classes = (IsAuthenticated, GlobalDefaultPermissions,)

    def get_serializer_class(self):
        if self.request.method == "GET":
            return ClinicHolidayListSerializer
        return ClinicHolidaySerializers



@extend_schema_view(
    get=extend_schema(
        description='Retorna os dados de uma férias específico',
        responses={200: ClinicHolidaySerializers},
        tags=['Férias Clínica']
    ),
    put=extend_schema(
        description='Atualiza todos os dados de uma férias',
        request=ClinicHolidaySerializers,
        responses={200: ClinicHolidaySerializers},
        tags=['Férias Clínica']
    ),
    patch=extend_schema(
        description='Atualiza parcialmente os dados de uma férias clínica',
        request=ClinicHolidaySerializers,
        responses={200: ClinicHolidaySerializers},
        tags=['Férias Clínica']
    ),
    delete=extend_schema(
        description='Remove um férias clínica do sistema',
        responses={204: None},
        tags=['Férias Clínica']
    )
)
class ClinicHolidayRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):

    queryset = ClinicHoliday.objects.all()
    permission_classes = (IsAuthenticated, GlobalDefaultPermissions,)

    def get_serializer_class(self):
        if self.request.method == "GET":
            return ClinicHolidayListSerializer
        return ClinicHolidaySerializers