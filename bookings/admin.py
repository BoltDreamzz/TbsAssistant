from django.contrib import admin
from .models import Appointment, Service, BlockedTime

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('user', 'service', 'date', 'time', 'paid')
    actions = ['reschedule', 'cancel']

admin.site.register(Service)
admin.site.register(BlockedTime)

from .models import Booking

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('name', 'date', 'time', 'service')
    search_fields = ('name', 'email', 'phone')
    list_filter = ('date', 'service')