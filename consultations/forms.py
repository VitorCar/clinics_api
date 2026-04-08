from django import forms
from .models import Consultation, Prescription
from scheduling.models import ScheduleAppointment


class ConsultationForm(forms.ModelForm):
    class Meta:
        model = Consultation
        fields = ['appointment', 'clinical_notes', 'disease_history', 'physical_examination', 'service_Status', 'final_duration', 'digital_signature']
        
        widgets = {
            'appointment': forms.Select(attrs={'class': 'form-select'}),
            'clinical_notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Evolução clínica, queixas principais...'}),
            'disease_history': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Histórico familiar, comorbidades (HMA/HMP)...'}),
            'physical_examination': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Sinais vitais, exame físico geral...'}),
            'service_Status': forms.Select(attrs={'class': 'form-select'}),
            'final_duration': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: 00:45:00'}),
            'digital_signature': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Hash ou código da assinatura'}),
        }
        
        labels = {
            'appointment': 'Agendamento Vinculado',
            'clinical_notes': 'Anotações Clínicas / Evolução',
            'disease_history': 'História da Moléstia',
            'physical_examination': 'Exame Físico',
            'service_Status': 'Status do Atendimento',
            'final_duration': 'Duração Final da Consulta',
            'digital_signature': 'Assinatura Eletrônica',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if not self.instance.pk:
            self.fields['appointment'].queryset = ScheduleAppointment.objects.filter(visualizar_agendamento__isnull=True)
        else:
            self.fields['appointment'].queryset = ScheduleAppointment.objects.filter(visualizar_agendamento__isnull=True) | ScheduleAppointment.objects.filter(pk=self.instance.appointment.pk)


class PrescriptionForm(forms.ModelForm):
    class Meta:
        model = Prescription
        fields = ['consultation', 'medicines_name', 'dosage', 'frequency', 'duration', 'instructions']
        
        widgets = {
            'consultation': forms.Select(attrs={'class': 'form-select'}),
            'medicines_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Amoxicilina 500mg, Dipirona...'}),
            'dosage': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Ex: 1 comprimido, 5ml...'}),
            'frequency': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Ex: De 8 em 8 horas...'}),
            'duration': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: 7 dias, Uso contínuo...'}),
            'instructions': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Recomendações extras, tomar com alimentos...'}),
        }
        
        labels = {
            'consultation': 'Consulta / Prontuário Base',
            'medicines_name': 'Nome do Medicamento',
            'dosage': 'Dose (Posologia)',
            'frequency': 'Frequência',
            'duration': 'Duração do Tratamento',
            'instructions': 'Instruções Adicionais (Opcional)',
        }
