from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema_view, extend_schema
from .models import ScheduleAppointment
from .serializers import ScheduleAppointmentSerializers, ScheduleAppointmentListSerializers
from accounts.utils import is_professional, is_patient
from app.permissions import GlobalDefaultPermissions, IsOwnerOrClinic


@extend_schema_view(
    get=extend_schema(
        description='Retorna todos os agendamentos e seus dados',
        responses={200: ScheduleAppointmentSerializers},
        tags=['Agendar_Consultas']
    ),
    post=extend_schema(
        description='Criar um agendamento de consulta',
        request=ScheduleAppointmentSerializers,
        responses={201: ScheduleAppointmentSerializers},
        tags=['Agendar_Consultas']
    )
)
class ScheduleAppointmentListCreateAPIView(ListCreateAPIView):

    permission_classes = (IsAuthenticated, GlobalDefaultPermissions,)

    

    def get_queryset(self):

        user = self.request.user

        queryset = ScheduleAppointment.objects.select_related(
            "professional__user",
            "patient__user",
            "clinic"
        )

        # PROFISSIONAL
        if is_professional(user):
            return queryset.filter(
                professional=user.professional
            )

        # PACIENTE
        if is_patient(user):
            return queryset.filter(
                patient=user.patient
            )

        # CLÍNICA / ADMIN
        if user.is_staff:
            return queryset

        return ScheduleAppointment.objects.none()
    
    def get_serializer_class(self):
        if self.request.method == "GET":
            return ScheduleAppointmentListSerializers
        return ScheduleAppointmentSerializers


@extend_schema_view(
    get=extend_schema(
        description='Retorna os dados de um agendamento específico',
        responses={200: ScheduleAppointmentSerializers},
        tags=['Agendar_Consultas']
    ),
    put=extend_schema(
        description='Atualiza todos os dados de um agendamento',
        request=ScheduleAppointmentSerializers,
        responses={200: ScheduleAppointmentSerializers},
        tags=['Agendar_Consultas']
    ),
    patch=extend_schema(
        description='Atualiza parcialmente os dados de um agendamento',
        request=ScheduleAppointmentSerializers,
        responses={200: ScheduleAppointmentSerializers},
        tags=['Agendar_Consultas']
    ),
    delete=extend_schema(
        description='Remove um agendamento do sistema',
        responses={204: None},
        tags=['Agendar_Consultas']
    )
)
class ScheduleAppointmentRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):

    queryset = ScheduleAppointment.objects.all()
    permission_classes = (IsAuthenticated, GlobalDefaultPermissions, IsOwnerOrClinic,)
    
    def get_serializer_class(self):
        if self.request.method == "GET":
            return ScheduleAppointmentListSerializers
        return ScheduleAppointmentSerializers
