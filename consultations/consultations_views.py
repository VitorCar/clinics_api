from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema_view, extend_schema
from .models import Consultation
from .serializers import ConsultationSerializers, ConsultationListSerializers
from accounts.utils import is_patient, is_professional
from app.permissions import GlobalDefaultPermissions, IsOwnerOrClinic


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

    permission_classes = (IsAuthenticated, GlobalDefaultPermissions,)

    def get_queryset(self):
        user = self.request.user

       # PACIENTE
        if is_patient(user):
            return Consultation.objects.filter(
                appointment__patient=user.patient
            )

        # PROFISSIONAL
        if is_professional(user):
            return Consultation.objects.filter(
                appointment__professional=user.professional
            )

        # CLÍNICA / ADMIN
        if user.is_staff:
            return Consultation.objects.all()

        return Consultation.objects.none()

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
    permission_classes = (IsAuthenticated, GlobalDefaultPermissions, IsOwnerOrClinic,)

    def get_serializer_class(self):
        if self.request.method == "GET":
            return ConsultationListSerializers
        return ConsultationSerializers
