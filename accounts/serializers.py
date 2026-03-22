from rest_framework import serializers
from .models import CustomUsuario, Patients, HealthcareProfessional
from clinics.serializers import SpecialtySerializers


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUsuario
        fields = ['id','email', 'password', 'full_name', 'role']

class UserListSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUsuario
        fields = ['id','email', 'full_name', 'role']


class PatientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Patients
        fields = '__all__'


class PatientListSerializer(serializers.ModelSerializer):
    full_name = serializers.ReadOnlyField(source='user.full_name')
    email = serializers.ReadOnlyField(source='user.email')

    class Meta:
        model = Patients
        fields = [
            'id',
            'full_name',
            'email',
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
    full_name = serializers.ReadOnlyField(source='user.full_name')
    email = serializers.ReadOnlyField(source='user.email')
    specialty = SpecialtySerializers(many=True)

    class Meta:
        model = HealthcareProfessional
        fields = [
            'id',
            'full_name',
            'email',
            'cpf',
            'rg',
            'board_number',
            'state_of_issue_UF',
            'specialty',
            'digital_signature',
            'created_at',
            'updated_at',
        ]