import smtplib
from datetime import datetime, timedelta
import pytz
from apscheduler.schedulers.background import BackgroundScheduler

from django.conf import settings
from django.core.mail import send_mail
# from django.db.models import F

from main.models import Mailing, MessageMailing, AttemptMailing


def send_mailing():
    frequency_mailing = ["Разовая", "Раз в день", "Раз в неделю", "Раз в месяц"]
    zone = pytz.timezone(settings.TIME_ZONE)
    current_datetime = datetime.now(zone)
    mailings = Mailing.objects.filter(status_mailing="Запущена") #.filter(start_time=current_datetime)

    for mailing in mailings:
        status = False
        server_response = "Нет ответа"
        time_delta_mailing = current_datetime.day - mailing.start_time.day

        try:
            send_mail(
                    subject=MessageMailing.subject,
                    message=MessageMailing.body,
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[client.email for client in mailing.clients.all()],
                    fail_silently=False
            )
            if mailing.frequency_mailing == frequency_mailing[0]:
                mailing.status_mailing = "Завершена"
            if mailing.frequency_mailing == frequency_mailing[1]:
                mailing.start_time += timedelta(days=1)

            elif mailing.frequency == frequency_mailing[2] and time_delta_mailing >= 7:
                mailing.start_time += timedelta(days=7)

            elif mailing.frequency == frequency_mailing[3] and time_delta_mailing >= 30:
                mailing.start_time += timedelta(days=30)

            mailing.save()

            status = True
            server_response = "Успешно"

        except smtplib.SMTPResponseException as response:
            status = False
            server_response = str(response)

        finally:
            AttemptMailing.objects.create(
                mailing=mailing,
                status_mailing=status,
                server_response=server_response,
            )


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(send_mailing, "interval", seconds=10)
    scheduler.start()
