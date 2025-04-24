from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Appointment, Service
from datetime import datetime, time, timedelta

@api_view(['GET'])
def available_slots(request):
    date = request.query_params.get('date')
    service_id = request.query_params.get('service_id')
    service = Service.objects.get(id=service_id)
    taken = Appointment.objects.filter(date=date).values_list('time', flat=True)

    slots = []
    current = time(9, 0)
    end = time(17, 0)

    while datetime.combine(datetime.today(), current) < datetime.combine(datetime.today(), end):
        if current not in taken:
            slots.append(current.strftime("%H:%M"))
        dt = (datetime.combine(datetime.today(), current) + service.duration)
        current = dt.time()
    
    return Response(slots)
