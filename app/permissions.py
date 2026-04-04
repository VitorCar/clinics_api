from rest_framework import permissions
from accounts.utils import is_patient, is_professional


class GlobalDefaultPermissions(permissions.BasePermission):

    def has_permission(self, request, view):

        queryset = getattr(view, "queryset", None)

        if queryset is None:
            return True

        model = queryset.model

        action_map = {
            'GET': 'view',
            'POST': 'add',
            'PUT': 'change',
            'PATCH': 'change',
            'DELETE': 'delete',
            'OPTIONS': 'view',
            'HEAD': 'view',
        }

        action = action_map.get(request.method)

        if not action:
            return False

        perm = f'{model._meta.app_label}.{action}_{model._meta.model_name}'

        print("Checking perm:", perm)

        return request.user.has_perm(perm)


class IsOwnerOrClinic(permissions.BasePermission):
    """
    Object Level Permission

    Regras:
    - Admin/Clínica vê tudo
    - Paciente vê apenas seus dados
    - Profissional vê apenas dados relacionados a ele
    """

    def has_object_permission(self, request, view, obj):

        user = request.user

        # Clínica / Admin
        if user.is_staff:
            return True

        if hasattr(obj, "appointment"):
            appointment = obj.appointment

            if is_patient(user):
                return appointment.patient == user.patient

            if is_professional(user):
                return appointment.professional == user.professional

        if hasattr(obj, "consultation"):
            consultation = obj.consultation
            appointment = consultation.appointment

            if is_patient(user):
                return appointment.patient == user.patient

            if is_professional(user):
                return appointment.professional == user.healthcareprofessional

        if hasattr(obj, "patient") and hasattr(obj, "professional"):

            if is_patient(user):
                return obj.patient == user.patient

            if is_professional(user):
                return obj.professional == user.professional

        return False
