def user_context_processor(request):
    doctor_id = None
    if request.user.is_authenticated:
        doctor_id = request.user.doctor_id
    return {'doctor_id': doctor_id}
