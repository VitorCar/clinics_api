from rest_framework import serializers
from .models import Consultation, Prescription
from scheduling.serializers import ScheduleAppointmentListSerializers


class ConsultationSerializers(serializers.ModelSerializer):

    class Meta:
        model = Consultation
        fields = '__all__'


class ConsultationListSerializers(serializers.ModelSerializer):
    clinic_name = serializers.ReadOnlyField(source='appointment.clinic.name')
    clinic_phone = serializers.ReadOnlyField(source='appointment.clinic.phone')
    professional_name = serializers.ReadOnlyField(source='appointment.professional.user.full_name')
    specialty = serializers.StringRelatedField(
        source='appointment.professional.specialty', 
        many=True
    )

    class Meta:
        model = Consultation
        fields = [
            'id',
            'clinic_name',
            'clinic_phone',
            'professional_name',
            'specialty',
            'clinical_notes',
            'disease_history',
            'physical_examination',
            'service_Status',
            'final_duration',
            'digital_signature',
            'finalized_at',
            'created_at',
            'updated_at',
        ]


class PrescriptionSerializers(serializers.ModelSerializer):

    class Meta:
        model = Prescription
        fields = '__all__'


class PrescriptionListSerializers(serializers.ModelSerializer):
    clinic_name = serializers.ReadOnlyField(source='consultation.appointment.clinic.name')
    professional_name = serializers.ReadOnlyField(source='consultation.appointment.professional.user.full_name')
    professional_crm = serializers.ReadOnlyField(source='consultation.appointment.professional.board_number')
    specialties = serializers.StringRelatedField(
        source='consultation.appointment.professional.specialty', 
        many=True, 
        read_only=True
    )

    class Meta:
        model = Prescription
        fields = [
            'id',
            'clinic_name',
            'professional_name', 
            'professional_crm',
            'specialties',
            'medicines_name',
            'dosage',
            'frequency',
            'duration',
            'instructions',
            'created_at',
            'updated_at',
        ]
