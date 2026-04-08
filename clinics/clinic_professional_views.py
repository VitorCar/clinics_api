from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.db.models import Q
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema_view, extend_schema
from .models import ClinicProfessional
from .forms import ClinicProfessionalForm
from .serializers import ClinicProfessionalSerializers, ClinicProfessionalListSerializers
from app.permissions import GlobalDefaultPermissions


class ClinicProfessionalListView(ListView):
    model = ClinicProfessional
    template_name = 'clinic_professional_list.html'
    context_object_name = 'clinic_professionals'

    def get_queryset(self):
        queryset = super().get_queryset().select_related('clinic', 'professional__user').order_by('-start_date')
        
        q = self.request.GET.get('q')
        status = self.request.GET.get('status')

        if q:
            queryset = queryset.filter(
                Q(clinic__name__icontains=q) | 
                Q(professional__user__full_name__icontains=q)
            )
            
        if status == 'ativos':
            queryset = queryset.filter(active=True)
        elif status == 'inativos':
            queryset = queryset.filter(active=False)
            
        return queryset


class ClinicProfessionalCreateView(CreateView):
    model = ClinicProfessional
    form_class = ClinicProfessionalForm
    template_name = 'clinic_professional_create.html'
    success_url = reverse_lazy('clinic_professional_list')


class ClinicProfessionalUpdateView(UpdateView):
    model = ClinicProfessional
    form_class = ClinicProfessionalForm
    template_name = 'clinic_professional_create.html'
    success_url = reverse_lazy('clinic_professional_list')


class ClinicProfessionalDeleteView(DeleteView):
    model = ClinicProfessional
    template_name = 'clinic_professional_delete.html'
    success_url = reverse_lazy('clinic_professional_list')


@extend_schema_view(
    get=extend_schema(
        description='Retorna todos os dados da relação Clinica-Profissional ',
        responses={200: ClinicProfessionalSerializers},
        tags=['Clinica-Profissional']
    ),
    post=extend_schema(
        description='Criar uma relação Clinica-Profissional',
        request=ClinicProfessionalSerializers,
        responses={201: ClinicProfessionalSerializers},
        tags=['Clinica-Profissional']
    )
)
class ClinicProfessionalListCreateAPIView(ListCreateAPIView):

    queryset = ClinicProfessional.objects.all()
    permission_classes = (IsAuthenticated, GlobalDefaultPermissions,)
    
    def get_serializer_class(self):
        if self.request.method == "GET":
            return ClinicProfessionalListSerializers
        return ClinicProfessionalSerializers


@extend_schema_view(
    get=extend_schema(
        description='Retorna os dados de uma relação Clinica-Profissional específica',
        responses={200: ClinicProfessionalSerializers},
        tags=['Clinica-Profissional']
    ),
    put=extend_schema(
        description='Atualiza todos os dados de uma relação Clinica-Profissional',
        request=ClinicProfessionalSerializers,
        responses={200: ClinicProfessionalSerializers},
        tags=['Clinica-Profissional']
    ),
    patch=extend_schema(
        description='Atualiza parcialmente os dados de uma relação Clinica-Profissional',
        request=ClinicProfessionalSerializers,
        responses={200: ClinicProfessionalSerializers},
        tags=['Clinica-Profissional']
    ),
    delete=extend_schema(
        description='Remove uma relação Clinica-Profissional do sistema',
        responses={204: None},
        tags=['Clinica-Profissional']
    )
)
class ClinicProfessionalRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):

    queryset = ClinicProfessional.objects.all()
    permission_classes = (IsAuthenticated, GlobalDefaultPermissions,)

    def get_serializer_class(self):
        if self.request.method == "GET":
            return ClinicProfessionalListSerializers
        return ClinicProfessionalSerializers
