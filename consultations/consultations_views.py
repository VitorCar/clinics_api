from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.db.models import Q
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from drf_spectacular.utils import extend_schema_view, extend_schema
from .models import Consultation
from .forms import ConsultationForm
from .serializers import ConsultationSerializers, ConsultationListSerializers
from accounts.utils import is_patient, is_professional, is_admin
from app.permissions import GlobalDefaultPermissions, IsOwnerOrClinic


class ConsultationListView(LoginRequiredMixin, ListView):
    model = Consultation
    template_name = 'consultation_list.html'
    context_object_name = 'consultations'
    paginate_by = 10

    def get_queryset(self):
        user = self.request.user
        queryset = super().get_queryset().select_related(
            'appointment',
            'appointment__patient__user',
            'appointment__professional__user'
        ).order_by('-created_at')

        # ADMIN: vê todos (com filtros)
        if is_admin(user):
            q = self.request.GET.get('q')
            status_filter = self.request.GET.get('status')
            if q:
                queryset = queryset.filter(
                    Q(appointment__patient__user__full_name__icontains=q) |
                    Q(appointment__professional__user__full_name__icontains=q)
                )
            if status_filter:
                queryset = queryset.filter(service_Status=status_filter)
            return queryset

        # PACIENTE: vê apenas os seus prontuários
        if is_patient(user):
            return queryset.filter(appointment__patient=user.patient)

        # PROFISSIONAL: vê apenas os prontuários que ele atendeu
        if is_professional(user):
            return queryset.filter(appointment__professional=user.professional)

        return queryset.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['status_choices'] = Consultation.Status.choices
        context['can_create'] = is_admin(user := self.request.user) or is_professional(user)
        context['can_edit'] = context['can_create']
        context['can_delete'] = is_admin(self.request.user)
        return context


class ConsultationCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Consultation
    form_class = ConsultationForm
    template_name = 'consultation_create.html'
    success_url = reverse_lazy('consultation_list')

    def test_func(self):
        user = self.request.user
        return is_admin(user) or is_professional(user)


class ConsultationDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Consultation
    template_name = 'consultation_detail.html'
    context_object_name = 'consulta'

    def get_queryset(self):
        return super().get_queryset().select_related(
            'appointment__patient__user',
            'appointment__professional__user',
            'appointment__clinic'
        )

    def test_func(self):
        user = self.request.user
        if is_admin(user):
            return True
        consulta = self.get_object()
        if is_patient(user):
            return consulta.appointment.patient == user.patient
        if is_professional(user):
            return consulta.appointment.professional == user.professional
        return False


class ConsultationUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Consultation
    form_class = ConsultationForm
    template_name = 'consultation_create.html'
    success_url = reverse_lazy('consultation_list')

    def test_func(self):
        user = self.request.user
        if is_admin(user):
            return True
        if is_professional(user):
            return self.get_object().appointment.professional == user.professional
        return False

    def get_queryset(self):
        user = self.request.user
        qs = super().get_queryset()
        if is_admin(user):
            return qs
        if is_professional(user):
            return qs.filter(appointment__professional=user.professional)
        return qs.none()


class ConsultationDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Consultation
    template_name = 'consultation_delete.html'
    success_url = reverse_lazy('consultation_list')

    def test_func(self):
        user = self.request.user
        if is_admin(user):
            return True
        if is_professional(user):
            return self.get_object().appointment.professional == user.professional
        return False

    def get_queryset(self):
        user = self.request.user
        qs = super().get_queryset()
        if is_admin(user):
            return qs
        if is_professional(user):
            return qs.filter(appointment__professional=user.professional)
        return qs.none()


@extend_schema_view(
    get=extend_schema(
        description='Retorna todos as consultas e seus dados',
        responses={200: ConsultationSerializers},
        tags=['Consultas']
    ),
    post=extend_schema(
        description='Criar uma consulta',
        request=ConsultationSerializers,
        responses={201: ConsultationSerializers},
        tags=['Consultas']
    )
)
class ConsultationListCreateAPIView(ListCreateAPIView):

    permission_classes = (IsAuthenticated, GlobalDefaultPermissions,)

    filter_backends = [
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter,
    ]

    filterset_fields = [
        "service_Status",
        "created_at",
    ]

    search_fields = [
        "appointment__patient__user__full_name",
        "appointment__professional__user__full_name",
    ]

    ordering_fields = [
        "created_at",
        "finalized_at",
    ]

    ordering = ["-created_at"]

    def get_queryset(self):
        user = self.request.user

        # PACIENTE
        if is_patient(user):
            return Consultation.objects.filter(appointment__patient=user.patient)

        # PROFISSIONAL
        if is_professional(user):
            return Consultation.objects.filter(appointment__professional=user.professional)

        # CLÍNICA / ADMIN
        if is_admin(user):
            return Consultation.objects.all()

        return Consultation.objects.none()

    def get_serializer_class(self):
        if self.request.method == "GET":
            return ConsultationListSerializers
        return ConsultationSerializers


@extend_schema_view(
    get=extend_schema(
        description='Retorna os dados de uma consulta específico',
        responses={200: ConsultationSerializers},
        tags=['Consultas']
    ),
    put=extend_schema(
        description='Atualiza todos os dados de uma consulta',
        request=ConsultationSerializers,
        responses={200: ConsultationSerializers},
        tags=['Consultas']
    ),
    patch=extend_schema(
        description='Atualiza parcialmente os dados de uma consulta',
        request=ConsultationSerializers,
        responses={200: ConsultationSerializers},
        tags=['Consultas']
    ),
    delete=extend_schema(
        description='Remove uma consulta do sistema',
        responses={204: None},
        tags=['Consultas']
    )
)
class ConsultationRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):

    queryset = Consultation.objects.all()
    permission_classes = (IsAuthenticated, GlobalDefaultPermissions, IsOwnerOrClinic,)

    def get_serializer_class(self):
        if self.request.method == "GET":
            return ConsultationListSerializers
        return ConsultationSerializers