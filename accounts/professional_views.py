from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import AllowAny
from drf_spectacular.utils import extend_schema_view, extend_schema
from  .models import HealthcareProfessional
from .serializers import ProfessionalSerializer, ProfessionalListSerializer


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

    queryset = HealthcareProfessional.objects.all()
    permission_classes = (AllowAny,)
    
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
    permission_classes = (AllowAny,)

    def get_serializer_class(self):
        if self.request.method == "GET":
            return ProfessionalListSerializer
        return ProfessionalSerializer
