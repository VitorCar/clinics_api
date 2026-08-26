from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.db.models import Q
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from drf_spectacular.utils import extend_schema_view, extend_schema
from .models import Prescription
from .forms import PrescriptionForm
from .serializers import PrescriptionSerializers, PrescriptionListSerializers
from accounts.utils import is_patient, is_professional, is_admin
from app.permissions import GlobalDefaultPermissions, IsOwnerOrClinic


class PrescriptionListView(LoginRequiredMixin, ListView):
    model = Prescription
    template_name = 'prescription_list.html'
    context_object_name = 'prescriptions'
    paginate_by = 10

    def get_queryset(self):
        user = self.request.user
        queryset = super().get_queryset().select_related(
            'consultation__appointment__patient__user',
            'consultation__appointment__professional__user'
        ).order_by('-created_at')

        # ADMIN: vê todos (com filtros de busca)
        if is_admin(user):
            q = self.request.GET.get('q')
            if q:
                queryset = queryset.filter(
                    Q(medicines_name__icontains=q) |
                    Q(consultation__appointment__patient__user__full_name__icontains=q)
                )
            return queryset

        # PACIENTE: vê apenas suas receitas
        if is_patient(user):
            return queryset.filter(consultation__appointment__patient=user.patient)

        # PROFISSIONAL: vê receitas que ele prescreveu
        if is_professional(user):
            return queryset.filter(consultation__appointment__professional=user.professional)

        return queryset.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['can_create'] = is_admin(user := self.request.user) or is_professional(user)
        context['can_edit'] = context['can_create']
        context['can_delete'] = is_admin(self.request.user)
        return context


class PrescriptionCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Prescription
    form_class = PrescriptionForm
    template_name = 'prescription_create.html'
    success_url = reverse_lazy('prescription_list')

    def test_func(self):
        user = self.request.user
        return is_admin(user) or is_professional(user)


class PrescriptionUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Prescription
    form_class = PrescriptionForm
    template_name = 'prescription_create.html'
    success_url = reverse_lazy('prescription_list')

    def test_func(self):
        user = self.request.user
        if is_admin(user):
            return True
        if is_professional(user):
            return self.get_object().consultation.appointment.professional == user.professional
        return False

    def get_queryset(self):
        user = self.request.user
        qs = super().get_queryset()
        if is_admin(user):
            return qs
        if is_professional(user):
            return qs.filter(consultation__appointment__professional=user.professional)
        return qs.none()


class PrescriptionDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Prescription
    template_name = 'prescription_delete.html'
    success_url = reverse_lazy('prescription_list')

    def test_func(self):
        user = self.request.user
        if is_admin(user):
            return True
        if is_professional(user):
            return self.get_object().consultation.appointment.professional == user.professional
        return False

    def get_queryset(self):
        user = self.request.user
        qs = super().get_queryset()
        if is_admin(user):
            return qs
        if is_professional(user):
            return qs.filter(consultation__appointment__professional=user.professional)
        return qs.none()


class PrescriptionDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Prescription
    template_name = 'prescription_detail.html'
    context_object_name = 'prescription'

    def get_queryset(self):
        return super().get_queryset().select_related(
            'consultation__appointment__patient__user',
            'consultation__appointment__professional__user',
            'consultation__appointment__clinic'
        )

    def test_func(self):
        user = self.request.user
        if is_admin(user):
            return True
        presc = self.get_object()
        if is_patient(user):
            return presc.consultation.appointment.patient == user.patient
        if is_professional(user):
            return presc.consultation.appointment.professional == user.professional
        return False


@extend_schema_view(
    get=extend_schema(
        description='Retorna todos as prescrições e seus dados',
        responses={200: PrescriptionSerializers},
        tags=['Prescrições']
    ),
    post=extend_schema(
        description='Criar uma prescrição',
        request=PrescriptionSerializers,
        responses={201: PrescriptionSerializers},
        tags=['Prescrições']
    )
)
class PrescriptionListCreateAPIView(ListCreateAPIView):

    permission_classes = (IsAuthenticated, GlobalDefaultPermissions,)

    filter_backends = [
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter,
    ]

    filterset_fields = [
        "created_at",
    ]

    search_fields = [
        "consultation__appointment__patient__user__full_name",
        "consultation__appointment__professional__user__full_name",
    ]

    ordering_fields = [
        "created_at",
    ]

    ordering = ["-created_at"]

    def get_queryset(self):
        user = self.request.user
        queryset = Prescription.objects.select_related(
            "consultation__appointment__patient__user",
            "consultation__appointment__professional__user",
        )

        # PACIENTE
        if is_patient(user):
            return queryset.filter(consultation__appointment__patient=user.patient)

        # PROFISSIONAL
        if is_professional(user):
            return queryset.filter(consultation__appointment__professional=user.professional)

        # CLÍNICA / ADMIN
        if is_admin(user):
            return queryset

        return Prescription.objects.none()

    def get_serializer_class(self):
        if self.request.method == "GET":
            return PrescriptionListSerializers
        return PrescriptionSerializers


@extend_schema_view(
    get=extend_schema(
        description='Retorna os dados de uma prescrição específica',
        responses={200: PrescriptionSerializers},
        tags=['Prescrições']
    ),
    put=extend_schema(
        description='Atualiza todos os dados de uma prescrição',
        request=PrescriptionSerializers,
        responses={200: PrescriptionSerializers},
        tags=['Prescrições']
    ),
    patch=extend_schema(
        description='Atualiza parcialmente os dados de uma prescrição',
        request=PrescriptionSerializers,
        responses={200: PrescriptionSerializers},
        tags=['Prescrições']
    ),
    delete=extend_schema(
        description='Remove uma prescrição do sistema',
        responses={204: None},
        tags=['Prescrições']
    )
)
class PrescriptionRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):

    queryset = Prescription.objects.all()
    permission_classes = (IsAuthenticated, GlobalDefaultPermissions, IsOwnerOrClinic,)

    def get_serializer_class(self):
        if self.request.method == "GET":
            return PrescriptionListSerializers
        return PrescriptionSerializers