from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import AllowAny
from drf_spectacular.utils import extend_schema_view, extend_schema
from .models import Patients
from .serializers import PatientSerializer, PatientListSerializer


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

    queryset = Patients.objects.all()
    permission_classes = (AllowAny,)
    
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
    permission_classes = (AllowAny,)

    def get_serializer_class(self):
        if self.request.method == "GET":
            return PatientListSerializer
        return PatientSerializer
