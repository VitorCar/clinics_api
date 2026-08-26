from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.db.models import Q
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema_view, extend_schema
from .models import Specialty
from .forms import SpecialtyForm
from .serializers import SpecialtySerializers
from app.permissions import GlobalDefaultPermissions
from accounts.utils import is_admin


class SpecialtyListView(LoginRequiredMixin, ListView):
    model = Specialty
    template_name = 'specialty_list.html'
    context_object_name = 'specialties'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset().order_by('name')

        # ADMIN: permite busca
        if is_admin(self.request.user):
            q = self.request.GET.get('q')
            if q:
                queryset = queryset.filter(Q(name__icontains=q) | Q(description__icontains=q))
            return queryset

        # PACIENTE/PROFISSIONAL: vê todas as especialidades
        return queryset


class SpecialtyCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Specialty
    form_class = SpecialtyForm
    template_name = 'specialty_create.html'
    success_url = reverse_lazy('specialty_list')

    def test_func(self):
        return is_admin(self.request.user)


class SpecialtyUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Specialty
    form_class = SpecialtyForm
    template_name = 'specialty_create.html'
    success_url = reverse_lazy('specialty_list')

    def test_func(self):
        return is_admin(self.request.user)


class SpecialtyDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Specialty
    template_name = 'specialty_delete.html'
    success_url = reverse_lazy('specialty_list')

    def test_func(self):
        return is_admin(self.request.user)


@extend_schema_view(
    get=extend_schema(
        description='Retorna todas as especialidades e seus dados',
        responses={200: SpecialtySerializers},
        tags=['Especialidades']
    ),
    post=extend_schema(
        description='Adicionar uma especialidade',
        request=SpecialtySerializers,
        responses={201: SpecialtySerializers},
        tags=['Especialidades']
    )
)
class SpecialtyListCreateAPIView(ListCreateAPIView):

    queryset = Specialty.objects.all()
    permission_classes = (IsAuthenticated, GlobalDefaultPermissions,)
    serializer_class = SpecialtySerializers


@extend_schema_view(
    get=extend_schema(
        description='Retorna os dados de uma especialidade específico',
        responses={200: SpecialtySerializers},
        tags=['Especialidades']
    ),
    put=extend_schema(
        description='Atualiza todos os dados de uma especialidade',
        request=SpecialtySerializers,
        responses={200: SpecialtySerializers},
        tags=['Especialidades']
    ),
    patch=extend_schema(
        description='Atualiza parcialmente os dados de uma especialidade',
        request=SpecialtySerializers,
        responses={200: SpecialtySerializers},
        tags=['Especialidades']
    ),
    delete=extend_schema(
        description='Remove uma especialidade do sistema',
        responses={204: None},
        tags=['Especialidades']
    )
)
class SpecialtyRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):

    queryset = Specialty.objects.all()
    permission_classes = (IsAuthenticated, GlobalDefaultPermissions,)
    serializer_class = SpecialtySerializers