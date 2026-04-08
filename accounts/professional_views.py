from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.db.models import Q
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema_view, extend_schema
from .models import HealthcareProfessional
from .forms import HealthcareProfessionalForm
from .serializers import ProfessionalSerializer, ProfessionalListSerializer
from .utils import is_professional
from app.permissions import GlobalDefaultPermissions


class ProfessionalListView(ListView):
    model = HealthcareProfessional
    template_name = 'professional_list.html'
    context_object_name = 'professionals'

    def get_queryset(self):
        queryset = super().get_queryset().select_related('user').prefetch_related('specialty').order_by('-created_at')
        
        q = self.request.GET.get('q')
        if q:
            queryset = queryset.filter(
                Q(user__full_name__icontains=q) | 
                Q(cpf__icontains=q) |
                Q(board_number__icontains=q)
            )
        return queryset
    

class ProfessionalCreateView(CreateView):
    model = HealthcareProfessional
    form_class = HealthcareProfessionalForm
    template_name = 'professional_create.html'
    success_url = reverse_lazy('professional_list')


class ProfessionalUpdateView(UpdateView):
    model = HealthcareProfessional
    form_class = HealthcareProfessionalForm
    template_name = 'professional_create.html'
    success_url = reverse_lazy('professional_list')


class ProfessionalDeleteView(DeleteView):
    model = HealthcareProfessional
    template_name = 'professional_delete.html'
    success_url = reverse_lazy('professional_list')


@extend_schema_view(
    get=extend_schema(
        description='Retorna todos os profissionais e seus dados',
        responses={200: ProfessionalSerializer},
        tags=['Profissionais']
    ),
    post=extend_schema(
        description='Criar a indentificação de um profissional da saúde',
        request=ProfessionalSerializer,
        responses={201: ProfessionalSerializer},
        tags=['Profissionais']
    )
)
class ProfessionalListCreateApiView(ListCreateAPIView):

    permission_classes = (IsAuthenticated, GlobalDefaultPermissions,)

    def get_queryset(self):
        user = self.request.user
        if is_professional(user):
            return HealthcareProfessional.objects.filter(user=user)
    
    def get_serializer_class(self):
        if self.request.method == "GET":
            return ProfessionalListSerializer
        return ProfessionalSerializer


@extend_schema_view(
    get=extend_schema(
        description='Retorna os dados de um profissional da saúde específico',
        responses={200: ProfessionalSerializer},
        tags=['Profissionais']
    ),
    put=extend_schema(
        description='Atualiza todos os dados de um profissional da saúde',
        request=ProfessionalSerializer,
        responses={200: ProfessionalSerializer},
        tags=['Profissionais']
    ),
    patch=extend_schema(
        description='Atualiza parcialmente os dados de um profissional da saúde',
        request=ProfessionalSerializer,
        responses={200: ProfessionalSerializer},
        tags=['Profissionais']
    ),
    delete=extend_schema(
        description='Remove um profissional da saúde do sistema',
        responses={204: None},
        tags=['Profissionais']
    )
)
class ProfessionalRetrieveUpdateDestroyApiView(RetrieveUpdateDestroyAPIView):

    queryset = HealthcareProfessional.objects.all()
    permission_classes = (IsAuthenticated, GlobalDefaultPermissions,)

    def get_serializer_class(self):
        if self.request.method == "GET":
            return ProfessionalListSerializer
        return ProfessionalSerializer
