from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema_view, extend_schema
from .models import ClinicProfessional
from .serializers import ClinicProfessionalSerializers, ClinicProfessionalListSerializers


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
    permission_classes = (IsAuthenticated,)
    
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
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        if self.request.method == "GET":
            return ClinicProfessionalListSerializers
        return ClinicProfessionalSerializers
