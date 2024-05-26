import smtplib
from datetime import datetime, timedelta
import pytz
from apscheduler.schedulers.background import BackgroundScheduler

from django.conf import settings
from django.core.mail import send_mail

from main.models import Mailing, AttemptMailing


def send_mailing():
    # print("Запущена попытка рассылок")
    frequency_mailing = ["Разовая", "Раз в день", "Раз в неделю", "Раз в месяц"]
    zone = pytz.timezone(settings.TIME_ZONE)
    current_datetime = datetime.now(zone)
    mailings = Mailing.objects.filter(status_mailing__in=["Создана", "Запущена"], start_time__lte=current_datetime, is_active=True)

    for mailing in mailings:
        status = False
        server_response = "Нет ответа"
        last_successful_attempt = AttemptMailing.objects.filter(mailing=mailing.pk, status=True).last()
        if last_successful_attempt:
            time_last_successful_attempt = last_successful_attempt.time_last_mailing
        else:
            time_last_successful_attempt = mailing.start_time
        time_delta_mailing = (current_datetime - time_last_successful_attempt).days

        if mailing.stop_time < current_datetime:
            mailing.status_mailing = "Завершена"
            mailing.save()
            continue

        is_time_mailing = False  # Признак наступления времени запуска рассылки
        if mailing.status_mailing == "Создана":
            is_time_mailing = True
            mailing.status_mailing = "Запущена"
        if mailing.frequency_mailing == frequency_mailing[0]:
            is_time_mailing = True
            mailing.status_mailing = "Завершена"

        elif mailing.frequency_mailing == frequency_mailing[1] and time_delta_mailing >= 1:
            # mailing.start_time += timedelta(days=1)
            is_time_mailing = True
        elif mailing.frequency_mailing == frequency_mailing[2] and time_delta_mailing >= 7:
            # mailing.start_time += timedelta(days=7)
            is_time_mailing = True
        elif mailing.frequency_mailing == frequency_mailing[3] and time_delta_mailing >= 30:
            # mailing.start_time += timedelta(days=30)
            is_time_mailing = True

        if is_time_mailing:
            try:
                send_mail(
                        subject=mailing.message.subject,
                        message=mailing.message.body,
                        from_email=settings.EMAIL_HOST_USER,
                        recipient_list=[client.email for client in mailing.clients.all()],
                        fail_silently=False
                )

                # if mailing.status_mailing == "Создана":
                #     mailing.status_mailing = "Запущена"
                # if mailing.frequency_mailing == frequency_mailing[0]:
                #     mailing.status_mailing = "Завершена"
                # if mailing.frequency_mailing == frequency_mailing[1] and time_delta_mailing >= 1:
                #     mailing.start_time += timedelta(days=1)
                #
                # elif mailing.frequency_mailing == frequency_mailing[2] and time_delta_mailing >= 7:
                #     mailing.start_time += timedelta(days=7)
                #
                # elif mailing.frequency_mailing == frequency_mailing[3] and time_delta_mailing >= 30:
                #     mailing.start_time += timedelta(days=30)

                status = True
                server_response = "Успешно"

                if mailing.frequency_mailing == frequency_mailing[0]:
                    mailing.status_mailing = "Завершена"

                mailing.save()

            except smtplib.SMTPResponseException as response:
                status = False
                server_response = str(response)

            finally:
                AttemptMailing.objects.create(
                    mailing=mailing,
                    status=status,
                    server_response=server_response,
                )


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(send_mailing, 'interval', seconds=60)
    scheduler.start()