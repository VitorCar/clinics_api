from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.db.models import Q
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema_view, extend_schema
from .models import Clinic
from .forms import ClinicForm
from .serializers import ClinicSerializers
from app.permissions import GlobalDefaultPermissions


class ClinicListView(ListView):
    model = Clinic
    template_name = 'clinic_list.html'
    context_object_name = 'clinics'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset().order_by('name')
        
        q = self.request.GET.get('q')
        status_filter = self.request.GET.get('status')

        if q:
            queryset = queryset.filter(Q(name__icontains=q) | Q(cnpj__icontains=q))
        if status_filter:
            queryset = queryset.filter(status=status_filter)
            
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Passa as opções de status para o <select> do filtro no HTML
        context['status_choices'] = Clinic.Status.choices
        return context


class ClinicCreateView(CreateView):
    model = Clinic
    form_class = ClinicForm
    template_name = 'clinic_create.html'
    success_url = reverse_lazy('clinic_list')


class ClinicUpdateView(UpdateView):
    model = Clinic
    form_class = ClinicForm
    template_name = 'clinic_create.html'
    success_url = reverse_lazy('clinic_list')


class ClinicDeleteView(DeleteView):
    model = Clinic
    template_name = 'clinic_delete.html'
    success_url = reverse_lazy('clinic_list')


@extend_schema_view(
    get=extend_schema(
        description='Retorna todos as clínicas e seus dados',
        responses={200: ClinicSerializers},
        tags=['Clinicas']
    ),
    post=extend_schema(
        description='Adicionar uma clínica',
        request=ClinicSerializers,
        responses={201: ClinicSerializers},
        tags=['Clinicas']
    )
)
class ClinicListCreateAPIView(ListCreateAPIView):

    queryset = Clinic.objects.all()
    permission_classes = (IsAuthenticated, GlobalDefaultPermissions,)
    serializer_class = ClinicSerializers


@extend_schema_view(
    get=extend_schema(
        description='Retorna os dados de uma clínica específico',
        responses={200: ClinicSerializers},
        tags=['Clinicas']
    ),
    put=extend_schema(
        description='Atualiza todos os dados de uma clínica',
        request=ClinicSerializers,
        responses={200: ClinicSerializers},
        tags=['Clinicas']
    ),
    patch=extend_schema(
        description='Atualiza parcialmente os dados de uma clínica',
        request=ClinicSerializers,
        responses={200: ClinicSerializers},
        tags=['Clinicas']
    ),
    delete=extend_schema(
        description='Remove uma clínica do sistema',
        responses={204: None},
        tags=['Clinicas']
    )
)
class ClinicRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):

    queryset = Clinic.objects.all()
    permission_classes = (IsAuthenticated, GlobalDefaultPermissions,)
    serializer_class = ClinicSerializers
