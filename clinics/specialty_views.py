from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema_view, extend_schema
from .models import Specialty
from .serializers import SpecialtySerializers


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
    permission_classes = (IsAuthenticated,)
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
    permission_classes = (IsAuthenticated,)
    serializer_class = SpecialtySerializers
