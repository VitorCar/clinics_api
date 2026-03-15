from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import AllowAny
from drf_spectacular.utils import extend_schema_view, extend_schema
from .models import ScheduleAppointment
from .serializers import ScheduleAppointmentSerializers, ScheduleAppointmentListSerializers


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

    queryset = ScheduleAppointment.objects.all()
    permission_classes = (AllowAny,)
    
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
    permission_classes = (AllowAny,)
    
    def get_serializer_class(self):
        if self.request.method == "GET":
            return ScheduleAppointmentListSerializers
        return ScheduleAppointmentSerializers
