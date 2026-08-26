from accounts.models import Patients, HealthcareProfessional


def is_patient(user):
    return user.is_authenticated and Patients.objects.filter(user=user).exists()


def is_professional(user):
    return user.is_authenticated and HealthcareProfessional.objects.filter(user=user).exists()


def is_clinic(user):
    return user.is_staff


def is_admin(user):
    return user.is_authenticated and (user.is_staff or user.is_superuser or user.role == 'ADMIN')


def can_manage(user):
    return is_admin(user)


def is_owner_patient(user, obj):
    return is_patient(user) and getattr(obj, 'patient', None) == user.patient


def is_owner_professional(user, obj):
    return is_professional(user) and getattr(obj, 'professional', None) == user.professional