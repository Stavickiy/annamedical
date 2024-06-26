import re
from celery import shared_task
from django.utils import timezone
from twilio.rest import Client
from datetime import timedelta
from appointment.models import Appointment
import requests
import json
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def validate_and_format_phone_number(phone_number):
    # Удаляем все символы, кроме цифр
    cleaned_phone_number = re.sub(r'\D', '', phone_number)

    # Проверяем и форматируем номер
    if cleaned_phone_number.startswith('8'):
        cleaned_phone_number = '7' + cleaned_phone_number[1:]
    elif cleaned_phone_number.startswith("38071"):
        cleaned_phone_number = '7949' + cleaned_phone_number[5:]
    elif not cleaned_phone_number.startswith('7'):
        return None

    # Регулярное выражение для проверки валидности номера
    pattern = re.compile(r'^7[0-9]{10}$')
    if pattern.match(cleaned_phone_number):
        return cleaned_phone_number
    else:
        return None

@shared_task
def send_reminders():
    # URL с параметрами
    url = "https://admin.p1sms.ru/apiSms/create"
    api_key = "Oda8dkcQtXlehryWQvHKEiaeKz7QAbC1SQNJ4CAKkx4nYciPNnLJr4Q61rqi"

    # Текущее время
    now = timezone.now()

    # Начало и конец следующего дня
    tomorrow_start = (now + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
    tomorrow_end = tomorrow_start + timedelta(days=1)

    # Выборка посещений на следующий день
    upcoming_appointments = Appointment.objects.filter(start__gte=tomorrow_start, start__lt=tomorrow_end)

    headers = {
        "Content-Type": "application/json"
    }

    sms_list = []


    for appointment in upcoming_appointments:
        if appointment.clinic.name == 'Донецк' and \
                appointment.status != 'canceled' and \
                appointment.type == 'primary':
            patient = appointment.patient
            doctor = appointment.doctor

            phone_number = validate_and_format_phone_number(patient.phone_number)
            if phone_number:
                message = f"Напоминаем о вашем приеме у стоматолога {doctor} {appointment.start.strftime('%d/%m %H:%M')}"
                # message = "Отбеливание зубов-скидка 30%! \nЗаписаться: https://t.me/stavickayaanna"
                sms_data = {
                    "phone": phone_number,
                    "text": message,
                    "channel": 'char',
                    "sender": 'AS_Smiles',
                }
                sms_list.append(sms_data)

    payload = {
        "apiKey": api_key,
        "sms": sms_list
    }

    # Отправка POST-запроса
    response = requests.post(url, headers=headers, data=json.dumps(payload))

    # Проверка статуса ответа
    if response.status_code == 200:
        logger.info(f'Сообщение отправлено успешно. Ответ сервера смс: {response}')
        logger.info(response.text)
    else:
        logger.error(f'Ошибка: {response.status_code}')
        logger.error(response.text)