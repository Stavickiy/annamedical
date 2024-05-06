from appointment.models import Appointment
from datetime import datetime, timedelta

def user_context_processor(request):
    doctor_id = None
    if request.user.is_authenticated:
        doctor_id = request.user.doctor_id
    return {'doctor_id': doctor_id}

def count_appointments_processor(request):
    if request.user.is_authenticated:
        # Получаем текущую дату без учета времени
        current_date = datetime.now().date()
        # Определяем начальную и конечную дату для фильтрации записей на сегодня
        start_of_day = datetime.combine(current_date, datetime.min.time())
        end_of_day = datetime.combine(current_date, datetime.max.time())
        # Фильтруем записи Appointment по полю start
        appointments_by_doctor_today = Appointment.objects.filter(doctor=request.user.doctor, start__range=(start_of_day, end_of_day))
        return {'appointments_by_doctor_today': appointments_by_doctor_today}
    return {}
