from accounts.models import Patients
from accounts.models import HealthcareProfessional

def is_patient(user):
    return Patients.objects.filter(user=user).exists()


def is_professional(user):
    return HealthcareProfessional.objects.filter(user=user).exists()


def is_clinic(user):
    return user.is_staff
