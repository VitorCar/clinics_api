from django.db import models
from accounts.models import Patients, HealthcareProfessional
from clinics.models import Clinic
import datetime
from datetime import timedelta


class ScheduleAppointment(models.Model):

    class Status(models.TextChoices):
        AGENDADO = 'AGENDADO', 'Agendado'
        CONFIRMADO = 'CONFIRMADO', 'Confirmado'
        CONCLUIDO = 'CONCLUIDO', 'Concluido'
        CANCELADO = 'CANCELADO', 'Cancelado'
        AUSENTE = 'AUSENTE', 'Ausente'

    patient = models.ForeignKey(Patients, on_delete=models.CASCADE, related_name='Agendar_consulta_patient')
    professional = models.ForeignKey(HealthcareProfessional,
                                        on_delete=models.CASCADE,
                                        related_name='Agendar_consulta_profissional')
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE, related_name='Agendar_consulta_clinica')
    scheduled_date = models.DateField() # "2023-12-25"
    scheduled_time = models.TimeField() # "14:30:00"
    status = models.CharField(max_length=15, choices=Status.choices, default=Status.AGENDADO)
    reason_for_consultation = models.TextField(blank=True, null=True)
    average_duration = models.DurationField(default=timedelta(minutes=30)) # "00:30:00"
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Evitar dois pacientes no mesmo horário.
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["professional", "scheduled_date", "scheduled_time"],
                name="unique_professional_schedule"
            )
        ]

    def __str__(self):
        return self.patient.user.full_name


class ClinicSchedule(models.Model):

    class WeekDays(models.IntegerChoices):
        SEGUNDA = 1, 'Segunda'
        TERÇA = 2, 'Terça'
        QUARTA = 3, 'Quarta'
        QUINTA = 4, 'Quinta'
        SEXTA = 5, 'Sexta'
        SABADO = 6, 'Sabado'
        DOMINGO = 7, 'Domingo'

    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE, related_name='clinica_agenda')
    days_week = models.IntegerField(choices=WeekDays.choices)
    date = models.DateField(default=datetime.date.today)
    open_time = models.TimeField()
    close_time = models.TimeField()
    is_open = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.clinic.name}"


class ClinicHoliday(models.Model):

    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE, related_name='clinica_feriado')
    date = models.DateField()
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.clinic.name
