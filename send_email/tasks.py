from celery import shared_task
from django.shortcuts import render
from django.http import HttpResponse
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
from clinics.models import Clinic
from scheduling.models import ScheduleAppointment


@shared_task
def send_weekly_task_summary():
    today = timezone.now().date()
    last_week = today - timedelta(days=7)
    active_clinics = Clinic.objects.filter(status='ATIVA')
    emails_sent = 0

    for clinic in active_clinics:
        appointments = ScheduleAppointment.objects.filter(
            clinic=clinic,
            scheduled_date__gte=last_week,
            scheduled_date__lt=today
        )
        total_consultas = appointments.count()
        concluidos = appointments.filter(status='CONCLUIDO').count()
        cancelados = appointments.filter(status='CANCELADO').count()
        taxa_sucesso = (concluidos / total_consultas * 100) if total_consultas > 0 else 0

        contexto = {
            'clinica': clinic,
            'inicio_semana': last_week.strftime('%d/%m/%Y'),
            'fim_semana': (today - timedelta(days=1)).strftime('%d/%m/%Y'),
            'total_consultas': total_consultas,
            'concluidos': concluidos,
            'cancelados': cancelados,
            'taxa_sucesso': round(taxa_sucesso, 1)
        }

        html_content = render_to_string('emails/weekly_summary.html', contexto)
        subject = f"📊 Resumo Semanal - {clinic.name}"
        sender = settings.EMAIL_HOST_USER
        recipient = [clinic.email]

        msg = EmailMultiAlternatives(
            subject=subject,
            body="Por favor, abra este e-mail em um cliente compatível com HTML.",
            from_email=sender,
            to=recipient
        )
        msg.attach_alternative(html_content, "text/html")
        msg.send()
        emails_sent += 1
        
    return f"{emails_sent} e-mails processados com sucesso."
