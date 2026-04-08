from django import forms
from .models import Specialty, Clinic, ClinicProfessional


class SpecialtyForm(forms.ModelForm):
    class Meta:
        model = Specialty
        fields = ['name', 'description']
        
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Cardiologia, Pediatria...'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Descrição opcional sobre a especialidade...'}),
        }
        
        labels = {
            'name': 'Nome da Especialidade',
            'description': 'Descrição / Observações',
        }


class ClinicForm(forms.ModelForm):
    class Meta:
        model = Clinic
        fields = ['name', 'cnpj', 'address', 'phone', 'email', 'status']
        
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome da Clínica ou Unidade'}),
            'cnpj': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '00.000.000/0000-00'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Rua, Número, Bairro, Cidade - Estado'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '(00) 0000-0000'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'contato@clinica.com'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
        }
        
        labels = {
            'name': 'Nome da Clínica',
            'cnpj': 'CNPJ',
            'address': 'Endereço Completo',
            'phone': 'Telefone Comercial',
            'email': 'E-mail de Contato',
            'status': 'Status da Clínica',
        }


class ClinicProfessionalForm(forms.ModelForm):
    class Meta:
        model = ClinicProfessional
        fields = ['clinic', 'professional', 'start_date', 'end_date', 'active']
        
        widgets = {
            'clinic': forms.Select(attrs={'class': 'form-select'}),
            'professional': forms.Select(attrs={'class': 'form-select'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'active': forms.CheckboxInput(attrs={'class': 'form-check-input', 'role': 'switch'}),
        }
        
        labels = {
            'clinic': 'Clínica / Unidade',
            'professional': 'Profissional de Saúde',
            'start_date': 'Data de Início do Vínculo',
            'end_date': 'Data de Término (Opcional)',
            'active': 'Vínculo Ativo?',
        }
