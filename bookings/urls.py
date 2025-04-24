from django.urls import path
from . import views

app_name = 'bookings'

urlpatterns = [
    path('', views.index, name='index'),
    path('checkout/', views.create_checkout_session, name='create_checkout_session'),
    path('success/', views.payment_success, name='payment_success'),
    path('cancel/', views.payment_cancel, name='payment_cancel'),
    path('available-slots/', views.available_slots, name='available_slots'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('booking/<uuid:booking_id>/', views.booking_detail, name='booking_detail'),
    path('booking/<uuid:booking_id>/download-ics/', views.download_ics, name='download_ics')
    # path('booking/<uuid:booking_id>/cancel/', views.cancel_booking, name='cancel_booking'),


    ]

from .views import stripe_webhook

urlpatterns += [
    path('webhook/', stripe_webhook, name='stripe_webhook'),
]
#                 'product_data': {'name': service.name},