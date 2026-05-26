from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUsuario, HealthcareProfessional, Patients
from.forms import CustomUsuarioCreationForm, CustomUsuarioChangeForm



@admin.register(CustomUsuario)
class CustomUsuarioAdmin(UserAdmin):

    add_form = CustomUsuarioCreationForm
    form = CustomUsuarioChangeForm
    model = CustomUsuario

    list_display = (
        'email',
        'full_name',
        'role',
        'is_staff',
        'is_active'
    )

    list_filter = (
        'role',
        'is_staff',
        'is_active',
        'is_superuser'
    )

    search_fields = (
        'email',
        'full_name'
    )

    ordering = ('email',)

    readonly_fields = (
        'date_joined',
        'last_login'
    )

    fieldsets = (
        ('Credenciais de Acesso', {
            'fields': ('email', 'password')
        }),

        ('Informações Pessoais', {
            'fields': ('full_name', 'role')
        }),

        ('Permissões e Status', {
            'fields': (
                'is_active',
                'is_staff',
                'is_superuser',
                'groups',
                'user_permissions'
            )
        }),

        ('Datas Importantes', {
            'fields': (
                'last_login',
                'date_joined'
            )
        }),
    )


    add_fieldsets = (
        ('Dados do Novo Usuário', {
            'classes': ('wide',),
            'fields': (
                'email',
                'full_name',
                'role',
                'password',
                'is_staff',
                'is_active'
            ),
        }),
    )


@admin.register(Patients)
class PatientsAdmin(admin.ModelAdmin):

    list_display = ('id', 'cpf', 'birth_date', 'phone', 'created_at', 'updated_at')
    search_fields = ('id', 'cpf',)


@admin.register(HealthcareProfessional)
class HealthcareProfessionalAdmin(admin.ModelAdmin):

    list_display = ('id', 'cpf', 'rg', 'board_number', 'state_of_issue_UF', 'digital_signature', 'created_at', 'updated_at')
    search_fields = ('id', 'cpf', 'state_of_issue_UF', 'digital_signature',)
