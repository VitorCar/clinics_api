from django import forms
from .models import ClinicSchedule, ClinicHoliday, ScheduleAppointment

class ClinicScheduleForm(forms.ModelForm):
    class Meta:
        model = ClinicSchedule
        fields = ['clinic', 'days_week', 'date', 'open_time', 'close_time', 'is_open']
        
        widgets = {
            'clinic': forms.Select(attrs={'class': 'form-select'}),
            'days_week': forms.Select(attrs={'class': 'form-select'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'open_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'close_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'is_open': forms.CheckboxInput(attrs={'class': 'form-check-input', 'role': 'switch'}),
        }

        labels = {
            'clinic': 'Clínica',
            'days_week': 'Dia da Semana',
            'date': 'Data Específica',
            'open_time': 'Horário de Abertura',
            'close_time': 'Horário de Fechamento',
            'is_open': 'Clínica Aberta?',
        }


class ClinicHolidayForm(forms.ModelForm):
    class Meta:
        model = ClinicHoliday
        fields = ['clinic', 'date', 'description']
        
        widgets = {
            'clinic': forms.Select(attrs={'class': 'form-select'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Ex: Feriado Nacional, Reforma na Recepção...'}),
        }
        
        labels = {
            'clinic': 'Clínica',
            'date': 'Data do Feriado/Recesso',
            'description': 'Descrição / Motivo',
        }


class ScheduleAppointmentForm(forms.ModelForm):
    class Meta:
        model = ScheduleAppointment
        fields = ['patient', 'professional', 'clinic', 'scheduled_date', 'scheduled_time', 'average_duration', 'status', 'reason_for_consultation']
        
        widgets = {
            'patient': forms.Select(attrs={'class': 'form-select'}),
            'professional': forms.Select(attrs={'class': 'form-select'}),
            'clinic': forms.Select(attrs={'class': 'form-select'}),
            'scheduled_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'scheduled_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'average_duration': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '00:30:00 (HH:MM:SS)'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'reason_for_consultation': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Motivo da consulta, sintomas, primeira vez...'}),
        }
        
        labels = {
            'patient': 'Paciente',
            'professional': 'Profissional',
            'clinic': 'Clínica',
            'scheduled_date': 'Data da Consulta',
            'scheduled_time': 'Horário',
            'average_duration': 'Duração Estimada',
            'status': 'Status do Agendamento',
            'reason_for_consultation': 'Motivo da Consulta (Opcional)',
        }
