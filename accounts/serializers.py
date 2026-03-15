from rest_framework import serializers
from .models import CustomUsuario, Patients, HealthcareProfessional
from clinics.serializers import SpecialtySerializers


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUsuario
        fields = ['id','email', 'password', 'full_name', 'role']


class PatientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Patients
        fields = '__all__'


class PatientListSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Patients
        fields = [
            'id',
            'user',
            'cpf',
            'birth_date',
            'phone',
            'created_at',
            'updated_at',
        ]


class ProfessionalSerializer(serializers.ModelSerializer):

    class Meta:
        model = HealthcareProfessional
        fields = '__all__'


class ProfessionalListSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    specialty = SpecialtySerializers(many=True)

    class Meta:
        model = HealthcareProfessional
        fields = [
            'id',
            'user',
            'cpf',
            'rg',
            'board_number',
            'state_of_issue_UF',
            'specialty',
            'digital_signature',
            'created_at',
            'updated_at',
        ]