from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema_view, extend_schema
from .models import ClinicSchedule
from .serializers import ClinicScheduleSerializers, ClinicScheduleListSerializers
from app.permissions import GlobalDefaultPermissions


@extend_schema_view(
    get=extend_schema(
        description='Retorna todos os agendamentos e seus dados',
        responses={200: ClinicScheduleSerializers},
        tags=['Agendamento Clínico']
    ),
    post=extend_schema(
        description='Criar um agendamento clínico',
        request=ClinicScheduleSerializers,
        responses={201: ClinicScheduleSerializers},
        tags=['Agendamento Clínico']
    )
)
class ClinicScheduleListCreateAPIView(ListCreateAPIView):

    queryset = ClinicSchedule.objects.all()
    permission_classes = (IsAuthenticated, GlobalDefaultPermissions,)
    
    def get_serializer_class(self):
        if self.request.method == "GET":
            return ClinicScheduleListSerializers
        return ClinicScheduleSerializers


@extend_schema_view(
    get=extend_schema(
        description='Retorna os dados de um agendamento clínico específico',
        responses={200: ClinicScheduleSerializers},
        tags=['Agendamento Clínico']
    ),
    put=extend_schema(
        description='Atualiza todos os dados de um agendamento clínico',
        request=ClinicScheduleSerializers,
        responses={200: ClinicScheduleSerializers},
        tags=['Agendamento Clínico']
    ),
    patch=extend_schema(
        description='Atualiza parcialmente os dados de um agendamento clínico',
        request=ClinicScheduleSerializers,
        responses={200: ClinicScheduleSerializers},
        tags=['Agendamento Clínico']
    ),
    delete=extend_schema(
        description='Remove um agendamento clínico do sistema',
        responses={204: None},
        tags=['Agendamento Clínico']
    )
)
class ClinicScheduleRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):

    queryset = ClinicSchedule.objects.all()
    permission_classes = (IsAuthenticated, GlobalDefaultPermissions,)
    serializer_class = ClinicScheduleSerializers
