from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, SetPasswordForm
from .models import CustomUsuario, Patients, HealthcareProfessional
from clinics.models import Specialty


class CustomUsuarioCreationForm(UserCreationForm):

    class Meta:
        model = CustomUsuario
        fields = (
            'email',
            'full_name',
            'role',
            'is_staff',
            'is_active'
        )


class CustomUsuarioChangeForm(UserChangeForm):

    class Meta:
        model = CustomUsuario
        fields = (
            'email',
            'full_name',
            'role',
            'is_active',
            'is_staff',
            'is_superuser'
        )


class CustomUsuarioCreationForm(forms.ModelForm):
    password = forms.CharField(
        label='Senha', 
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Digite uma senha segura'})
    )

    class Meta:
        model = CustomUsuario
        fields = ['email', 'full_name', 'role', 'is_active', 'is_staff']
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'exemplo@email.com'}),
            'full_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome completo'}),
            'role': forms.Select(attrs={'class': 'form-select'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input', 'role': 'switch'}),
            'is_staff': forms.CheckboxInput(attrs={'class': 'form-check-input', 'role': 'switch'}),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password']) # Criptografa a senha antes de salvar
        if commit:
            user.save()
        return user
    

class CustomSetPasswordForm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})


class CustomUsuarioChangeForm(forms.ModelForm):
    class Meta:
        model = CustomUsuario
        fields = ['email', 'full_name', 'role', 'is_active', 'is_staff']
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'role': forms.Select(attrs={'class': 'form-select'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input', 'role': 'switch'}),
            'is_staff': forms.CheckboxInput(attrs={'class': 'form-check-input', 'role': 'switch'}),
        }


class PatientForm(forms.ModelForm):
    class Meta:
        model = Patients
        fields = ['user', 'cpf', 'birth_date', 'phone']
        
        widgets = {
            'user': forms.Select(attrs={'class': 'form-select'}),
            'cpf': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Apenas números'}),
            'birth_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '(00) 00000-0000'}),
        }
        
        labels = {
            'user': 'Usuário Vinculado',
            'cpf': 'CPF',
            'birth_date': 'Data de Nascimento',
            'phone': 'Telefone / Celular',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        base_queryset = CustomUsuario.objects.filter(
            role=CustomUsuario.Roles.PACIENTE, 
            patient__isnull=True
        )

        if not self.instance.pk:
            self.fields['user'].queryset = base_queryset
        else:
            self.fields['user'].queryset = base_queryset | CustomUsuario.objects.filter(pk=self.instance.user.pk)

class HealthcareProfessionalForm(forms.ModelForm):
    class Meta:
        model = HealthcareProfessional
        fields = ['user', 'cpf', 'rg', 'board_number', 'state_of_issue_UF', 'specialty', 'digital_signature']
        
        widgets = {
            'user': forms.Select(attrs={'class': 'form-select'}),
            'cpf': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Apenas números'}),
            'rg': forms.TextInput(attrs={'class': 'form-control'}),
            'board_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: 123456'}),
            'state_of_issue_UF': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'SP, RJ, MG...', 'maxlength': '2'}),
            'specialty': forms.SelectMultiple(attrs={'class': 'form-select', 'size': 4}),
            'digital_signature': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Assinatura digital, carimbo ou hash...'}),
        }
        
        labels = {
            'user': 'Usuário Vinculado',
            'cpf': 'CPF',
            'rg': 'RG',
            'board_number': 'Número do Conselho (CRM/COREN)',
            'state_of_issue_UF': 'UF do Conselho',
            'specialty': 'Especialidades',
            'digital_signature': 'Assinatura Digital / Carimbo',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        base_queryset = CustomUsuario.objects.filter(
            role=CustomUsuario.Roles.PROFISSIONAL, 
            professional__isnull=True
        )

        if not self.instance.pk:
            self.fields['user'].queryset = base_queryset
        else:
            self.fields['user'].queryset = base_queryset | CustomUsuario.objects.filter(pk=self.instance.user.pk)
