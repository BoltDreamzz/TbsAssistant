# bookings/models.py
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Service(models.Model):
    name = models.CharField(max_length=100)
    duration = models.DurationField()  # e.g. 1 hour
    price = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return self.name

class BlockedTime(models.Model):
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f"{self.date} from {self.start_time} to {self.end_time}"

class Appointment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.SET_NULL, null=True)
    date = models.DateField()
    time = models.TimeField()
    paid = models.BooleanField(default=False)
    google_event_id = models.CharField(max_length=200, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.service.name} on {self.date} at {self.time}"
    

import uuid

class Booking(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    service = models.ForeignKey('Service', on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    created_at = models.DateTimeField(default=timezone.now)
    stripe_session_id = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.name} - {self.date} {self.time}"
