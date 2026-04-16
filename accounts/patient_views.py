from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db.models import Q
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema_view, extend_schema
from .models import Patients
from .forms import PatientForm
from .serializers import PatientSerializer, PatientListSerializer
from .utils import is_patient
from app.permissions import GlobalDefaultPermissions


class PatientListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Patients
    template_name = 'patient_list.html'
    context_object_name = 'patients'
    paginate_by = 10
    permission_required = 'accounts.view_patients'

    def get_queryset(self):
        user = self.request.user
        queryset = super().get_queryset().select_related('user').order_by('-created_at')

        if user.role == 'PACIENTE':
            # O paciente só vê os agendamentos onde ele é o dono
            return queryset.filter(user=user)
        
        elif user.role == 'PROFISSIONAL':
            # O médico só vê os agendamentos marcados para ele
            return queryset
        
        q = self.request.GET.get('q')
        if q:
            queryset = queryset.filter(Q(user__full_name__icontains=q) | Q(cpf__icontains=q))
            
        return queryset


class PatientCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Patients
    form_class = PatientForm
    template_name = 'patient_create.html'
    success_url = reverse_lazy('patient_list')
    permission_required = 'accounts.add_patients'


class PatientUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Patients
    form_class = PatientForm
    template_name = 'patient_create.html'
    success_url = reverse_lazy('patient_list')
    permission_required = 'accounts.change_patients'

    def get_queryset(self):
        user = self.request.user
        if user.role == 'PACIENTE':
            return Patients.objects.filter(patient__user=user)
        elif user.role == 'PROFISSIONAL':
            return Patients.objects.filter(professional__user=user)
        return Patients.objects.all()


class PatientDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Patients
    template_name = 'patient_delete.html'
    success_url = reverse_lazy('patient_list')
    permission_required = 'accounts.delete_patients'


@extend_schema_view(
    get=extend_schema(
        description='Retorna todos os pacientes e seus dados',
        responses={200: PatientSerializer},
        tags=['Pacientes']
    ),
    post=extend_schema(
        description='Criar dados de um paciente',
        request=PatientSerializer,
        responses={201: PatientSerializer},
        tags=['Pacientes']
    )
)
class PatientListCreateApiView(ListCreateAPIView):

    permission_classes = (IsAuthenticated, GlobalDefaultPermissions,)

    def get_queryset(self):
        user = self.request.user
        if is_patient(user):
            return Patients.objects.filter(user=user)
        
    
    def get_serializer_class(self):
        if self.request.method == "GET":
            return PatientListSerializer
        return PatientSerializer


@extend_schema_view(
    get=extend_schema(
        description='Retorna os dados de um paciente específico',
        responses={200: PatientSerializer},
        tags=['Pacientes']
    ),
    put=extend_schema(
        description='Atualiza todos os dados de um paciente',
        request=PatientSerializer,
        responses={200: PatientSerializer},
        tags=['Pacientes']
    ),
    patch=extend_schema(
        description='Atualiza parcialmente os dados de um paciente',
        request=PatientSerializer,
        responses={200: PatientSerializer},
        tags=['Pacientes']
    ),
    delete=extend_schema(
        description='Remove um paciente do sistema',
        responses={204: None},
        tags=['Pacientes']
    )
)
class PatientRetrieveUpdateDestroyApiView(RetrieveUpdateDestroyAPIView):

    queryset = Patients.objects.all()
    permission_classes = (IsAuthenticated, GlobalDefaultPermissions,)

    def get_serializer_class(self):
        if self.request.method == "GET":
            return PatientListSerializer
        return PatientSerializer
