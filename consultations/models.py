from django.db import models
from scheduling.models import ScheduleAppointment


class Consultation(models.Model):

    class Status(models.TextChoices):
        ATENDIDO = 'ATENDIDO', 'Atendido'
        FALTOU = 'FALTOU', 'Faltou'
        REMARCAR = 'REMARCAR', 'Remarcar'

    appointment = models.OneToOneField(ScheduleAppointment, on_delete=models.CASCADE, related_name='visualizar_agendamento')
    clinical_notes = models.TextField(blank=True, null=True)
    disease_history = models.TextField(blank=True, null=True)
    physical_examination = models.TextField(blank=True, null=True)
    service_Status = models.CharField(max_length=15, choices=Status.choices, default=Status.ATENDIDO)
    final_duration = models.DurationField(null=True, blank=True)
    digital_signature = models.TextField(blank=True, null=True)
    finalized_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.patient.user.full_name} - {self.professional.user.full_name}"
    

class Prescription(models.Model):

    consultation = models.ForeignKey(Consultation, on_delete=models.CASCADE, related_name='visualizar_consulta')
    medicines_name = models.CharField(max_length=255)
    dosage = models.TextField(max_length=255)
    frequency = models.TextField(max_length=255)
    duration = models.CharField(max_length=255)
    instructions = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.consultation.appointment.patient.user.full_name} - {self.medicines_name}"
