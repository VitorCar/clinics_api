from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import AllowAny
from drf_spectacular.utils import extend_schema_view, extend_schema
from .models import Clinic
from .serializers import ClinicSerializers


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
    permission_classes = (AllowAny,)
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
    permission_classes = (AllowAny,)
    serializer_class = ClinicSerializers
