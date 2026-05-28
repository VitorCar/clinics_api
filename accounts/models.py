from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from clinics.models import Specialty


# Como o usuário sera criado
class MyUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email: 
            raise ValueError('O e-mail é obrigatório')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        if not password:
            raise ValueError("Users must have a password")

        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', CustomUsuario.Roles.ADMIN)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser precisa ter is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser precisa ter is_superuser=True.')
        if extra_fields.get('role') != 'ADMIN':
            raise ValueError('Superuser precisa ter role="ADMIN".')
        
        return self.create_user(email, password, **extra_fields)
    

class CustomUsuario(AbstractBaseUser, PermissionsMixin):

    class Roles(models.TextChoices):
        ADMIN = 'ADMIN', 'Admin'
        PROFISSIONAL = 'PROFISSIONAL', 'Profissional'
        PACIENTE = 'PACIENTE', 'Paciente'

    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=255, blank=True, null=True)
    role = models.CharField(max_length=20, choices=Roles.choices, default=Roles.PACIENTE)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [] 

    def __str__(self):
        return self.email


class Patients(models.Model):
    
    user = models.OneToOneField(CustomUsuario, on_delete=models.CASCADE, related_name='patient')
    cpf = models.CharField(max_length=11 ,unique=True, null=True, blank=True)
    birth_date = models.DateField(blank=True, null=True)
    phone = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.full_name} ({self.user.email})"


class HealthcareProfessional(models.Model):
    
    user = models.OneToOneField(CustomUsuario, on_delete=models.CASCADE, related_name='professional')
    cpf = models.CharField(max_length=11 ,unique=True, null=True, blank=True)
    rg = models.CharField(max_length=15, blank=True, null=True)
    board_number = models.CharField(max_length=20, verbose_name="Número do Conselho")
    state_of_issue_UF = models.CharField(max_length=3, blank=True, null=True, verbose_name="Estado(UF) do Conselho")
    specialty = models.ManyToManyField(Specialty, related_name="professionals")
    digital_signature = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.full_name} ({self.user.email})"
