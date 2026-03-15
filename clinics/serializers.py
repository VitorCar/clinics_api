from rest_framework import serializers
from .models import Clinic, Specialty, ClinicProfessional


class ClinicSerializers(serializers.ModelSerializer):

    class Meta:
        model = Clinic
        fields = '__all__'


class SpecialtySerializers(serializers.ModelSerializer):

    class Meta:
        model = Specialty
        fields = '__all__'


class ClinicProfessionalSerializers(serializers.ModelSerializer):

    class Meta:
        model = ClinicProfessional
        fields = '__all__'


class ClinicProfessionalListSerializers(serializers.ModelSerializer):
    clinic_name = serializers.ReadOnlyField(source='clinic.name')
    clinic_city = serializers.ReadOnlyField(source='clinic.address')
    professional_name = serializers.ReadOnlyField(source='professional.user.full_name')
    professional_board = serializers.ReadOnlyField(source='professional.board_number')
    specialties = serializers.StringRelatedField(
        source='professional.specialty', 
        many=True
    )
    

    class Meta:
        model = ClinicProfessional
        fields = [
            'id',
            'clinic_name',
            'clinic_city',
            'professional_name',
            'professional_board',
            'specialties',
            'start_date',
            'end_date',
            'active',
            'created_at',
            'updated_at',
        ]

     # Este método busca o serializer apenas quando a API é chamada
    def get_professional(self, obj):
            from accounts.serializers import ProfessionalListSerializer
            return ProfessionalListSerializer(obj.professional).data
