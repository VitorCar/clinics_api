from django.contrib import admin
from consultations.models import Consultation, Prescription


@admin.register(Consultation)
class ConsultationAdmin(admin.ModelAdmin):

    list_display = ('id', 'clinical_notes', 'disease_history', 'physical_examination', 'service_Status', 'final_duration',
                    'digital_signature', 'finalized_at', 'created_at', 'updated_at')
    search_fields = ('id',)


@admin.register(Prescription)
class PrescriptionAdmin(admin.ModelAdmin):

    list_display = ('id', 'medicines_name', 'dosage', 'frequency', 'duration', 'instructions', 'created_at', 'updated_at')
    search_fields = ('id', 'medicines_name',)
