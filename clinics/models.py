from django.db import models


class Clinic(models.Model):

    class Status(models.TextChoices):
        ATIVA = 'ATIVA', 'Ativa'
        INATIVA = 'INATIVA', 'Inativa'

    name = models.CharField(max_length=220)
    cnpj = models.CharField(max_length=18, verbose_name="CNPJ", unique=True)
    address = models.TextField()
    phone = models.CharField(max_length=20)
    email = models.EmailField(blank=True, null=True)
    status = models.CharField(max_length=15, choices=Status.choices, default=Status.ATIVA)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Specialty(models.Model):

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class ClinicProfessional(models.Model):

    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE, related_name='clinic_professionals')
    professional = models.ForeignKey(
        "accounts.HealthcareProfessional", 
        on_delete=models.CASCADE, 
        related_name='clinic_professionals'
        )
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Evitar duplicação de vínculo.
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['clinic', 'professional'],
                name="unique_clinic_professional"
            )
        ]


    def __str__(self):
        return f"{self.clinic.name} - {self.professional.user.full_name}"
