from django.views.generic import TemplateView
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin
from accounts.models import Patients, HealthcareProfessional
from clinics.models import Clinic
from scheduling.models import ScheduleAppointment


class DashboardHomeView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        hoje = timezone.now().date()
        user = self.request.user
        
        if user.role == 'ADMIN':
            context['total_pacientes'] = Patients.objects.count()
            context['total_profissionais'] = HealthcareProfessional.objects.count()
            context['clinicas_ativas'] = Clinic.objects.filter(status='ATIVA').count()
            
            agendamentos = ScheduleAppointment.objects.filter(scheduled_date=hoje)
            context['agendamentos_hoje_count'] = agendamentos.count()
            context['proximos_agendamentos'] = agendamentos.select_related(
                'patient__user', 'professional__user', 'clinic'
            ).order_by('scheduled_time')[:10]

        elif user.role == 'PROFISSIONAL':
            meus_agendamentos = ScheduleAppointment.objects.filter(
                professional__user=user, 
                scheduled_date=hoje
            )
            context['agendamentos_hoje_count'] = meus_agendamentos.count()
            
            context['seus_pacientes_count'] = Patients.objects.filter(
                visualizar_agendamento_paciente__professional__user=user
            ).distinct().count()
            
            context['minhas_clinicas_count'] = Clinic.objects.filter(
                clinics_professional__professional__user=user
            ).distinct().count()

            context['proximos_agendamentos'] = meus_agendamentos.select_related(
                'patient__user', 'clinic'
            ).order_by('scheduled_time')[:10]

        elif user.role == 'PACIENTE':
            meus_compromissos = ScheduleAppointment.objects.filter(
                patient__user=user,
                scheduled_date__gte=hoje
            )
            context['meus_agendamentos_count'] = meus_compromissos.count()
            context['proximos_agendamentos'] = meus_compromissos.select_related(
                'professional__user', 'clinic'
            ).order_by('scheduled_date', 'scheduled_time')[:10]
            
        return context
