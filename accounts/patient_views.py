from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.core.exceptions import PermissionDenied
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema_view, extend_schema
from .models import Patients
from .forms import PatientForm
from .serializers import PatientSerializer, PatientListSerializer
from .utils import is_patient, is_professional, is_admin
from app.permissions import GlobalDefaultPermissions


class PatientListView(LoginRequiredMixin, ListView):
    model = Patients
    template_name = 'patient_list.html'
    context_object_name = 'patients'
    paginate_by = 10

    def get_queryset(self):
        user = self.request.user
        queryset = super().get_queryset().select_related('user').order_by('-created_at')

        # ADMIN: vê todos (com filtros de busca)
        if is_admin(user):
            q = self.request.GET.get('q')
            if q:
                queryset = queryset.filter(Q(user__full_name__icontains=q) | Q(cpf__icontains=q))
            return queryset

        # PROFISSIONAL: vê apenas os pacientes que já tiveram agendamento com ele
        if is_professional(user):
            return queryset.filter(
                Agendar_consulta_patient__professional=user.professional
            ).distinct()

        # PACIENTE: vê apenas a sua própria ficha
        if is_patient(user):
            return queryset.filter(user=user)

        return queryset.none()


class PatientCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Patients
    form_class = PatientForm
    template_name = 'patient_create.html'
    success_url = reverse_lazy('patient_list')

    def test_func(self):
        return is_admin(self.request.user)


class PatientUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Patients
    form_class = PatientForm
    template_name = 'patient_create.html'
    success_url = reverse_lazy('patient_list')

    def test_func(self):
        user = self.request.user
        if is_admin(user):
            return True
        # Paciente só pode editar a própria ficha
        if is_patient(user):
            return self.get_object().user == user
        return False

    def get_queryset(self):
        user = self.request.user
        if is_admin(user):
            return Patients.objects.all()
        if is_patient(user):
            return Patients.objects.filter(user=user)
        return Patients.objects.none()


class PatientDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Patients
    template_name = 'patient_delete.html'
    success_url = reverse_lazy('patient_list')

    def test_func(self):
        return is_admin(self.request.user)


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
        if is_professional(user):
            return Patients.objects.filter(
                Agendar_consulta_patient__professional=user.professional
            ).distinct()
        if is_admin(user):
            return Patients.objects.all()
        return Patients.objects.none()
    
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