from rest_framework import serializers
from .models import ScheduleAppointment, ClinicSchedule, ClinicHoliday
from accounts.serializers import PatientListSerializer, ProfessionalListSerializer
from clinics.serializers import ClinicSerializers


class ScheduleAppointmentSerializers(serializers.ModelSerializer):

    class Meta:
        model = ScheduleAppointment
        fields = '__all__'


class ScheduleAppointmentListSerializers(serializers.ModelSerializer):
    clinic_name = serializers.ReadOnlyField(source='clinic.name')
    patient_name = serializers.ReadOnlyField(source='patient.user.full_name')
    patient_phone = serializers.ReadOnlyField(source='patient.phone')
    professional_name = serializers.ReadOnlyField(source='professional.user.full_name')
    specialties = serializers.StringRelatedField(
        source='professional.specialty', 
        many=True
    )


    class Meta:
        model = ScheduleAppointment
        fields = [
            'id',
            'clinic_name',
            'patient_name',
            'patient_phone',
            'professional_name',
            'specialties',
            'reason_for_consultation',
            'scheduled_date',
            'scheduled_time',
            'status',
            'average_duration',
            'created_at',
            'updated_at',
        ]


class ClinicScheduleSerializers(serializers.ModelSerializer):

    class Meta:
        model = ClinicSchedule
        fields = '__all__'


class ClinicScheduleListSerializers(serializers.ModelSerializer):
    clinic_name = serializers.ReadOnlyField(source='clinic.name')
    day_name = serializers.SerializerMethodField()

    class Meta:
        model = ClinicSchedule
        fields = [
            'id',
            'clinic_name',
            'day_name',
            'date',
            'open_time',
            'close_time',
            'is_open',
            'created_at',
            'updated_at',
        ]

    def get_day_name(self, obj):
        days = {
            1: "Segunda-feira",
            2: "Terça-feira",
            3: "Quarta-feira",
            4: "Quinta-feira",
            5: "Sexta-feira",
            6: "Sábado",
            7: "Domingo",
        }
        return days.get(obj.days_week, "Não informado")


class ClinicHolidaySerializers(serializers.ModelSerializer):

    class Meta:
        model = ClinicHoliday
        fields = '__all__'


class ClinicHolidayListSerializer(serializers.ModelSerializer):
    clinic_name = serializers.ReadOnlyField(source='clinic.name')

    class Meta:
        model = ClinicHoliday
        fields = [
            'id',
            'clinic_name',
            'date',
            'description',
            'created_at',
        ]
