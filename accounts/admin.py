from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUsuario

@admin.register(CustomUsuario)
class CustomUsuarioAdmin(UserAdmin):
    # Campos exibidos na lista principal
    list_display = ('email', 'full_name', 'role', 'is_staff', 'is_active')
    
    # Filtros laterais
    list_filter = ('role', 'is_staff', 'is_active')
    
    # Ordenação padrão
    ordering = ('email',)
    
    # Configuração dos campos dentro do formulário de edição
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Informações Pessoais', {'fields': ('full_name', 'role')}),
        ('Permissões', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Datas Importantes', {'fields': ('date_joined', 'update_at')}),
    )

    # Campos que aparecem ao criar um usuário novo no admin
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'full_name', 'role', 'password', 'is_staff', 'is_active'),
        }),
    )

    # Impede que o campo de data seja editado manualmente (já que tem auto_now_add)
    readonly_fields = ('date_joined', 'update_at')

    # Campo de busca
    search_fields = ('email', 'full_name')
