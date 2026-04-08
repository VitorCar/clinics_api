from django.shortcuts import render
from django.views.generic import TemplateView
from django.utils import timezone
from accounts.models import Patients, HealthcareProfessional
from clinics.models import Clinic
from scheduling.models import ScheduleAppointment


class DashboardHomeView(TemplateView):
    template_name = 'dashboard/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        hoje = timezone.now().date()
        
        context['total_pacientes'] = Patients.objects.count()
        context['total_profissionais'] = HealthcareProfessional.objects.count()
        context['clinicas_ativas'] = Clinic.objects.filter(status='ATIVA').count()
        
        agendamentos_hoje = ScheduleAppointment.objects.filter(scheduled_date=hoje)
        
        context['agendamentos_hoje_count'] = agendamentos_hoje.count()
        
        context['proximos_agendamentos'] = agendamentos_hoje.select_related(
            'patient__user', 'professional__user', 'clinic'
        ).order_by('scheduled_time')[:10]
        
        return context
