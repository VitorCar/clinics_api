from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import AllowAny
from drf_spectacular.utils import extend_schema_view, extend_schema
from .models import ClinicHoliday
from .serializers import ClinicHolidaySerializers, ClinicHolidayListSerializer


@extend_schema_view(
    get=extend_schema(
        description='Retorna todas as férias clínicas e seus dados',
        responses={200: ClinicHolidaySerializers},
        tags=['Férias Clínica']
    ),
    post=extend_schema(
        description='Criar uma férias clínica',
        request=ClinicHolidaySerializers,
        responses={201: ClinicHolidaySerializers},
        tags=['Férias Clínica']
    )
)
class ClinicHolidayListCreateAPIView(ListCreateAPIView):

    queryset = ClinicHoliday.objects.all()
    permission_classes = (AllowAny,)
    
    def get_serializer_class(self):
        if self.request.method == "GET":
            return ClinicHolidayListSerializer
        return ClinicHolidaySerializers



@extend_schema_view(
    get=extend_schema(
        description='Retorna os dados de uma férias específico',
        responses={200: ClinicHolidaySerializers},
        tags=['Férias Clínica']
    ),
    put=extend_schema(
        description='Atualiza todos os dados de uma férias',
        request=ClinicHolidaySerializers,
        responses={200: ClinicHolidaySerializers},
        tags=['Férias Clínica']
    ),
    patch=extend_schema(
        description='Atualiza parcialmente os dados de uma férias clínica',
        request=ClinicHolidaySerializers,
        responses={200: ClinicHolidaySerializers},
        tags=['Férias Clínica']
    ),
    delete=extend_schema(
        description='Remove um férias clínica do sistema',
        responses={204: None},
        tags=['Férias Clínica']
    )
)
class ClinicHolidayRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):

    queryset = ClinicHoliday.objects.all()
    permission_classes = (AllowAny,)
    
    def get_serializer_class(self):
        if self.request.method == "GET":
            return ClinicHolidayListSerializer
        return ClinicHolidaySerializers
