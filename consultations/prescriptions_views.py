from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema_view, extend_schema
from .models import Prescription
from .serializers import PrescriptionSerializers, PrescriptionListSerializers
from accounts.utils import is_patient, is_professional
from app.permissions import GlobalDefaultPermissions


@extend_schema_view(
    get=extend_schema(
        description='Retorna todos as prescrições e seus dados',
        responses={200: PrescriptionSerializers},
        tags=['Prescrições']
    ),
    post=extend_schema(
        description='Criar uma prescrição',
        request=PrescriptionSerializers,
        responses={201: PrescriptionSerializers},
        tags=['Prescrições']
    )
)
class PrescriptionListCreateAPIView(ListCreateAPIView):

    permission_classes = (IsAuthenticated, GlobalDefaultPermissions,)

    def get_queryset(self):

        user = self.request.user

        queryset = Prescription.objects.select_related(
            "consultation__appointment__patient__user",
            "consultation__appointment__professional__user",
        )

        # PACIENTE
        if is_patient(user):
            return queryset.filter(
                consultation__appointment__patient=user.patient
            )

        # PROFISSIONAL
        if is_professional(user):
            return queryset.filter(
                consultation__appointment__professional=user.professional
            )

        # CLÍNICA / ADMIN
        if user.is_staff:
            return queryset

        return Prescription.objects.none()
    
    def get_serializer_class(self):
        if self.request.method == "GET":
            return PrescriptionListSerializers
        return PrescriptionSerializers


@extend_schema_view(
    get=extend_schema(
        description='Retorna os dados de uma prescrição específica',
        responses={200: PrescriptionSerializers},
        tags=['Prescrições']
    ),
    put=extend_schema(
        description='Atualiza todos os dados de uma prescrição',
        request=PrescriptionSerializers,
        responses={200: PrescriptionSerializers},
        tags=['Prescrições']
    ),
    patch=extend_schema(
        description='Atualiza parcialmente os dados de uma prescrição',
        request=PrescriptionSerializers,
        responses={200: PrescriptionSerializers},
        tags=['Prescrições']
    ),
    delete=extend_schema(
        description='Remove uma prescrição do sistema',
        responses={204: None},
        tags=['Prescrições']
    )
)
class PrescriptionRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):

    queryset = Prescription.objects.all()
    permission_classes = (IsAuthenticated, GlobalDefaultPermissions,)
    
    def get_serializer_class(self):
        if self.request.method == "GET":
            return PrescriptionListSerializers
        return PrescriptionSerializers
