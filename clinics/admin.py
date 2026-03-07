from django.contrib import admin
from .models import Clinic, Specialty, ClinicProfessional


@admin.register(Clinic)
class ClinicAdmin(admin.ModelAdmin):

    list_display = ('id', 'name','cnpj', 'address', 'phone', 'email', 'status', 'created_at', 'updated_at')
    search_fields = ('name',)


@admin.register(Specialty)
class SpecialtyAdmin(admin.ModelAdmin):
    
    list_display = ('id', 'name', 'description', 'created_at', 'updated_at')
    search_fields = ('name',)


@admin.register(ClinicProfessional)
class ClinicProfessionalAdmin(admin.ModelAdmin):

    list_display = ('id', 'start_date', 'end_date', 'active', 'created_at', 'updated_at')
    search_fields = ('id',)
