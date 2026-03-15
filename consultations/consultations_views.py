from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import AllowAny
from drf_spectacular.utils import extend_schema_view, extend_schema
from .models import Consultation
from .serializers import ConsultationSerializers, ConsultationListSerializers


@extend_schema_view(
    get=extend_schema(
        description='Retorna todos as consultas e seus dados',
        responses={200: ConsultationSerializers},
        tags=['Consultas']
    ),
    post=extend_schema(
        description='Criar uma consulta',
        request=ConsultationSerializers,
        responses={201: ConsultationSerializers},
        tags=['Consultas']
    )
)
class ConsultationListCreateAPIView(ListCreateAPIView):

    queryset = Consultation.objects.all()
    permission_classes = (AllowAny,)

    def get_serializer_class(self):
        if self.request.method == "GET":
            return ConsultationListSerializers
        return ConsultationSerializers


@extend_schema_view(
    get=extend_schema(
        description='Retorna os dados de uma consulta específico',
        responses={200: ConsultationSerializers},
        tags=['Consultas']
    ),
    put=extend_schema(
        description='Atualiza todos os dados de uma consulta',
        request=ConsultationSerializers,
        responses={200: ConsultationSerializers},
        tags=['Consultas']
    ),
    patch=extend_schema(
        description='Atualiza parcialmente os dados de uma consulta',
        request=ConsultationSerializers,
        responses={200: ConsultationSerializers},
        tags=['Consultas']
    ),
    delete=extend_schema(
        description='Remove uma consulta do sistema',
        responses={204: None},
        tags=['Consultas']
    )
)
class ConsultationRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):

    queryset = Consultation.objects.all()
    permission_classes = (AllowAny,)

    def get_serializer_class(self):
        if self.request.method == "GET":
            return ConsultationListSerializers
        return ConsultationSerializers
