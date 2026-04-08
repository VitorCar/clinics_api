from django.db.models import Count, F
from rest_framework import views, response, status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from drf_spectacular.utils import extend_schema_view, extend_schema, OpenApiTypes
from .models import CustomUsuario, Patients, HealthcareProfessional
from clinics.models import Clinic, ClinicProfessional,Specialty
from consultations.models import Consultation, Prescription
from scheduling.models import ScheduleAppointment


@extend_schema_view(
    get=extend_schema(
        description='Retorna estatísticas da API',
        responses={200: OpenApiTypes.OBJECT},
        tags=['estatísticas']
    )
)
class StatsView(views.APIView):
    permission_classes = (IsAuthenticated, IsAdminUser,)

    def get(self, request):
        data = {
            'total_users': CustomUsuario.objects.count(),
            'total_patients': Patients.objects.count(),
            'total_professional': HealthcareProfessional.objects.count(),
            'total_clinics': Clinic.objects.count(),
            'total_specialty': Specialty.objects.count(),
            'total_consultations': Consultation.objects.count(),
            'total_prescriptions': Prescription.objects.count(),
            'total_appointments': ScheduleAppointment.objects.count(),
            
            'active_professional_links': ClinicProfessional.objects.filter(active=True).count(),
            'inactive_professional_links': ClinicProfessional.objects.filter(active=False).count(),
        }

        data['patient_consultation'] = list(
            Consultation.objects.values(nome=F('appointment__patient__user__full_name'))
            .annotate(total=Count('id')).order_by('-total')
        )

        data['patient_prescription'] = list(
            Prescription.objects.values(nome=F('consultation__appointment__patient__user__full_name'))
            .annotate(total=Count('id')).order_by('-total')
        )

        data['patient_appointments'] = list(
            ScheduleAppointment.objects.values(nome=F('patient__user__full_name'))
            .annotate(total=Count('id')).order_by('-total')
        )

        data['professional_appointments'] = list(
            ScheduleAppointment.objects.values(nome=F('professional__user__full_name'))
            .annotate(total=Count('id')).order_by('-total')
        )

        return response.Response(data, status=status.HTTP_200_OK)
