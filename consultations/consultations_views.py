from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.db.models import Q
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from drf_spectacular.utils import extend_schema_view, extend_schema
from .models import Consultation
from .forms import ConsultationForm
from .serializers import ConsultationSerializers, ConsultationListSerializers
from accounts.utils import is_patient, is_professional
from app.permissions import GlobalDefaultPermissions, IsOwnerOrClinic


class ConsultationListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Consultation
    template_name = 'consultation_list.html'
    context_object_name = 'consultations'
    paginate_by = 10
    permission_required = 'consultations.view_consultation'

    def get_queryset(self):
        user = self.request.user
        queryset = super().get_queryset().select_related(
            'appointment',
            'appointment__patient__user',
            'appointment__professional__user'
        ).order_by('-created_at')

        if user.role == 'PACIENTE':
            # Filtra através do agendamento vinculado ao prontuário
            return queryset.filter(appointment__patient__user=user)
        
        elif user.role == 'PROFISSIONAL':
            # Filtra prontuários criados por este médico
            return queryset.filter(appointment__professional__user=user)
        
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['status_choices'] = Consultation.Status.choices
        return context


class ConsultationCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Consultation
    form_class = ConsultationForm
    template_name = 'consultation_create.html'
    success_url = reverse_lazy('consultation_list')
    permission_required = 'consultations.add_consultation'


class ConsultationDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Consultation
    template_name = 'consultation_detail.html'
    context_object_name = 'consulta'
    permission_required = 'consultations.view_consultation'

    def get_queryset(self):
        return super().get_queryset().select_related(
            'appointment__patient__user',
            'appointment__professional__user',
            'appointment__clinic'
        )


class ConsultationUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Consultation
    form_class = ConsultationForm
    template_name = 'consultation_create.html'
    success_url = reverse_lazy('consultation_list')
    permission_required = 'consultations.change_consultation'

    def get_queryset(self):
        user = self.request.user
        queryset = super().get_queryset()

        if user.role == 'PROFISSIONAL':
            return queryset.filter(appointment__professional__user=user)
        
        if user.role == 'PACIENTE':
            return queryset.none()

        return queryset


class ConsultationDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Consultation
    template_name = 'consultation_delete.html'
    success_url = reverse_lazy('consultation_list')
    permission_required = 'consultations.delete_consultation'


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

    # FILTER
    filterset_fields = [
        "service_Status",
        "created_at",
    ]

    # SEARCH
    search_fields = [
        "appointment__patient__user__full_name",
        "appointment__professional__user__full_name",
    ]

    # ORDER
    ordering_fields = [
        "created_at",
        "finalized_at",
    ]

    ordering = ["-created_at"]

    def get_queryset(self):
        user = self.request.user

       # PACIENTE
        if is_patient(user):
            return Consultation.objects.filter(
                appointment__patient=user.patient
            )

        # PROFISSIONAL
        if is_professional(user):
            return Consultation.objects.filter(
                appointment__professional=user.professional
            )

        # CLÍNICA / ADMIN
        if user.is_staff:
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
