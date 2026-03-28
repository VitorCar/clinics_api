from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CustomUsuario, Patients, HealthcareProfessional


@receiver(post_save, sender=CustomUsuario)
def create_user_profile(sender, instance, created, **kwargs):

    if created:

        if instance.role == "PACIENTE":
            Patients.objects.create(user=instance)

        elif instance.role == "PROFISSIONAL":
            HealthcareProfessional.objects.create(user=instance)
