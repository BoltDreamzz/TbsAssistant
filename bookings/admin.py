from django.contrib import admin
from .models import Appointment, Service, BlockedTime

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('user', 'service', 'date', 'time', 'paid', 'created_at')
    list_filter = ('service', 'date', 'paid', 'created_at')
    search_fields = ('user__username', 'service__name')
    ordering = ('-created_at',)
    readonly_fields = ('google_event_id', 'created_at')

    fieldsets = (
        ("Client Info", {
            'fields': ('user', 'service')
        }),
        ("Appointment Details", {
            'fields': ('date', 'time', 'paid')
        }),
        ("System Info", {
            'fields': ('google_event_id', 'created_at')
        }),
    )
    
admin.site.register(Service)
admin.site.register(BlockedTime)

from .models import Booking

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('name', 'date', 'time', 'service')
    search_fields = ('name', 'email', 'phone')
    list_filter = ('date', 'service')