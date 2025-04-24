import stripe
from django.conf import settings
from django.shortcuts import redirect, render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from .models import Service
from django.http import HttpResponseBadRequest
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import BlockedTime
from .calendar_utils import create_event
from datetime import datetime, timedelta
from urllib.parse import urlencode, quote_plus
from icalendar import Calendar, Event



stripe.api_key = settings.STRIPE_SECRET_KEY

def generate_ics(booking):
    cal = Calendar()
    event = Event()
    event.add('summary', f'{booking.service.name} Appointment')
    event.add('dtstart', datetime.combine(booking.date, booking.time))
    event.add('dtend', datetime.combine(booking.date, booking.time) + timedelta(minutes=30))
    event.add('location', 'Your Business Address')
    event.add('description', f'Appointment with {booking.name}')
    cal.add_component(event)

    response = HttpResponse(cal.to_ical(), content_type='text/calendar')
    response['Content-Disposition'] = f'attachment; filename=appointment_{booking.id}.ics'
    return response


def generate_google_calendar_url(booking):
    event = {
    'action': 'TEMPLATE',
    'text': f'{booking.service.name} Appointment',
    'dates': f"{booking.date.strftime('%Y%m%d')}T{booking.time.strftime('%H%M00')}/{booking.date.strftime('%Y%m%d')}T{(datetime.combine(booking.date, booking.time) + timedelta(minutes=30)).strftime('%H%M00')}",
    'details': f'You have an upcoming Appointment with Treatment by Steph for a {booking.service.name} session. The appointment will be held on {booking.date.strftime("%A, %d %B %Y")} at {booking.time.strftime("%I:%M %p")}. Please arrive on time and be ready to enjoy our professional services. If you have any questions or need to reschedule, feel free to contact us.',
    'location': 'Ikorodu, Lagos',
    }

    return f"https://www.google.com/calendar/render?{urlencode(event, quote_via=quote_plus)}"


# def index(request):
#     services = Service.objects.all()
#     serv = services[:2]

#     if request.method == 'POST':
#         try:
#             service = Service.objects.get(id=request.POST.get('service'))
#             name = request.POST.get('name')
#             email = request.POST.get('email')
#             phone = request.POST.get('phone')
#             date = request.POST.get('date')
#             time = request.POST.get('time')

#             if not all([name, email, phone, date, time]):
#                 return HttpResponseBadRequest("All fields are required.")

#             booking_date = datetime.strptime(date, "%Y-%m-%d").date()

#             # Ensure booking is on a weekday (Mon–Fri)
#             if booking_date.weekday() >= 5:
#                 # return HttpResponseBadRequest("Bookings are only available Monday to Friday.")
#                 messages.error(request, "Bookings are only available Monday to Friday.")


#             # Parse the selected time into a datetime.time object
#             selected_time = datetime.strptime(time, "%H:%M").time()

#             # Check if there's a blocked time that includes this time
#             if BlockedTime.objects.filter(
#                 date=booking_date,
#                 start_time__lte=selected_time,
#                 end_time__gte=selected_time
#             ).exists():
#                 return HttpResponseBadRequest("This time slot is unavailable.")


#             # Limit to 5 bookings per day
#             if Booking.objects.filter(date=booking_date).count() >= 5:
#                 return HttpResponseBadRequest("Booking limit for this day has been reached.")

#             # Create booking (pending payment)
#             booking = Booking.objects.create(
#                 name=name,
#                 email=email,
#                 phone=phone,
#                 service=service,
#                 date=booking_date,
#                 time=time
#             )

#             # Create Stripe Checkout Session
#             # session = stripe.checkout.Session.create(
#             #     payment_method_types=['card'],
#             #     line_items=[{
#             #         'price_data': {
#             #             'currency': 'ngn',
#             #             'product_data': {
#             #                 'name': service.name,
#             #             },
#             #             'unit_amount': int(float(service.price) * 100), #'unit_amount': int(float(service.price) * 100),
#             #         },
#             #         'quantity': 1,
#             #     }],
#             #     mode='payment',
#             #     success_url='http://localhost:8000/success/',
#             #     cancel_url='http://localhost:8000/cancel/',
#             #     metadata={
#             #         'booking_id': str(booking.id)
#             #     }
#             # )

#             # # Save session ID
#             # booking.stripe_session_id = session.id
#             booking.save()

#             # return redirect(session.url, code=303)
#             return redirect('bookings:payment_success')  # Redirect to a success page

                
#         except Exception as e:
#             print("Error occurred:", e)
#             import traceback
#             traceback.print_exc()
#             return HttpResponseBadRequest(f"An error occurred: {e}")


#     return render(request, 'bookings/index.html', {'services': services, 'serv': serv})

from django.core.mail import send_mail, EmailMessage
from django.template.loader import render_to_string

def index(request):
    services = Service.objects.all()
    serv = services[:2]

    if request.method == 'POST':
        try:
            service_id = request.POST.get('service')
            name = request.POST.get('name')
            email = request.POST.get('email')
            phone = request.POST.get('phone')
            date_str = request.POST.get('date')
            time_str = request.POST.get('time')

            # Validate required fields
            if not all([service_id, name, email, phone, date_str, time_str]):
                return HttpResponseBadRequest("All fields are required.")

            service = Service.objects.get(id=service_id)
            booking_date = datetime.strptime(date_str, "%Y-%m-%d").date()

            # Check if booking is on a weekday (Mon–Fri)
            if booking_date.weekday() >= 6:
                messages.error(request, "Bookings are only available Monday to Friday.")
                return redirect('bookings:index')

            selected_time = datetime.strptime(time_str, "%H:%M").time()

            # Check if time is blocked
            if BlockedTime.objects.filter(
                date=booking_date,
                start_time__lte=selected_time,
                end_time__gte=selected_time
            ).exists():
                messages.error(request, "This time slot is unavailable.")
                return redirect('bookings:index')

            # # Limit to 5 bookings per day
            # if Booking.objects.filter(date=booking_date).count() >= 10:
            #     messages.error(request, "Booking limit for this day has been reached.")
            #     return redirect('bookings:index')

            # Create the booking
            booking = Booking.objects.create(
                name=name,
                email=email,
                phone=phone,
                service=service,
                date=booking_date,
                time=datetime.strptime(time_str, "%H:%M").time()

            )
            messages.success(request, "Booking created successfully.")

            # Send email to client
            client_subject = "Appointment Confirmation"
            client_message = render_to_string("bookings/emails/booking_confirmation.html", {'booking': booking})
            client_email = EmailMessage(client_subject, client_message, to=[email])
            client_email.content_subtype = "html"
            client_email.send()

            # Send email to admin
            admin_subject = f"New Booking - {booking.name}"
            admin_message = render_to_string("bookings/emails/admin_notification.html", {'booking': booking})
            admin_email = EmailMessage(admin_subject, admin_message, to=[settings.DEFAULT_FROM_EMAIL])
            admin_email.content_subtype = "html"
            admin_email.send()

            try:
                create_event(booking)
            except Exception as e:
                print("Calendar event creation failed:", e)

            # Generate Google Calendar link for user
            calendar_url = generate_google_calendar_url(booking)

            # Render confirmation page
            return render(request, 'bookings/booking_confirmed.html', {
                'booking': booking,
                'calendar_url': calendar_url
            })

        except Service.DoesNotExist:
            return HttpResponseBadRequest("Invalid service selected.")
        except Exception as e:
            print("Error occurred:", e)
            import traceback
            traceback.print_exc()
            return HttpResponseBadRequest(f"An error occurred: {e}")

    return render(request, 'bookings/index.html', {'services': services, 'serv': serv})


def booking_detail(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    return render(request, 'bookings/booking_detail.html', {'booking': booking})

def download_ics(request, booking_id):
    booking = Booking.objects.get(id=booking_id)  # Use `booking_id` here as needed (UUID or integer)
    return generate_ics(booking)  # Call your function


# @csrf_exempt
# def create_checkout_session(request):
#     if request.method == 'POST':
#         service_id = request.POST.get('service_id')
#         service = Service.objects.get(id=service_id)

#         session = stripe.checkout.Session.create(
#             payment_method_types=['card'],
#             line_items=[{
#                 'price_data': {
#                     'currency': 'ngn',
#                     'product_data': {'name': service.name},
#                     'unit_amount': int(service.price * 100),
#                 },
#                 'quantity': 1,
#             }],
#             mode='payment',
#             success_url='http://localhost:8000/success/',
#             cancel_url='http://localhost:8000/cancel/',
#         )
#         return redirect(session.url, code=303)
#     return redirect('/')

from .models import Booking

def create_checkout_session(request):
    if request.method == 'POST':
        service = Service.objects.get(id=request.POST['service_id'])
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        date = request.POST['date']
        time = request.POST['time']

        # Create a pending booking
        booking = Booking.objects.create(
            name=name,
            email=email,
            phone=phone,
            service=service,
            date=date,
            time=time
        )

        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'ngn',
                    'product_data': {'name': service.name},
                    'unit_amount': int(service.price * 100),
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url='http://localhost:8000/success/',
            cancel_url='http://localhost:8000/cancel/',
            metadata={
                'booking_id': str(booking.id)
            }
        )

        booking.stripe_session_id = session.id
        booking.save()

        return redirect(session.url, code=303)


def payment_success(request):
    return render(request, 'bookings/success.html')


def payment_cancel(request):
    return render(request, 'bookings/cancel.html')


import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Booking
from .google_calendar import add_to_calendar  # 👈 You'll create this soon
from .utils import send_booking_email, send_sms


@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    endpoint_secret = settings.STRIPE_WEBHOOK_SECRET

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
    except (ValueError, stripe.error.SignatureVerificationError):
        return HttpResponse(status=400)

    # Handle successful payment
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        booking_id = session['metadata']['booking_id']
        booking = Booking.objects.get(id=booking_id)

        # Sync to Google Calendar
        add_to_calendar(booking)

        # Send emails/SMS (later)
        # Inside stripe_webhook after add_to_calendar()
        subject = 'Appointment Confirmed'
        message = f"Hi {booking.name}, your booking for {booking.service.name} on {booking.date} at {booking.time} is confirmed."

        send_booking_email(subject, message, booking.email)
        send_sms(message, booking.phone)
        # send_email(booking)
        # send_sms(booking)

    return HttpResponse(status=200)


from datetime import date

@login_required
def dashboard(request):
    bookings = Booking.objects.filter(email=request.user.email).order_by('-date', '-time')
    upcoming = bookings.filter(date__gte=date.today())
    past = bookings.filter(date__lt=date.today())

    context = {
        'upcoming': upcoming,
        'past': past,
    }
    return render(request, 'bookings/dashboard.html', context)


from django.http import JsonResponse


@csrf_exempt
def available_slots(request):
    date_str = request.GET.get('date')  # e.g. '2025-04-24'
    selected_date = datetime.strptime(date_str, "%Y-%m-%d").date()
    slots = ['10:00', '11:00', '12:00', '13:00', '14:00']  # You can adjust these

    if selected_date.weekday() >= 5:
        return JsonResponse({'slots': []})

    booked = Booking.objects.filter(date=selected_date).values_list('time', flat=True)
    blocked = BlockedTime.objects.filter(date=selected_date).values_list('time', flat=True)

    available = [s for s in slots if s not in [b.strftime('%H:%M') for b in booked] and s not in [b.strftime('%H:%M') for b in blocked]]

    return JsonResponse({'slots': available})


from .forms import RescheduleRequestForm
from django.contrib import messages
from django.core.mail import send_mail

@login_required
def request_reschedule(request, booking_id):
    booking = Booking.objects.get(id=booking_id, email=request.user.email)

    if request.method == 'POST':
        form = RescheduleRequestForm(request.POST)
        if form.is_valid():
            msg = form.cleaned_data['message']
            send_mail(
                f'Reschedule Request from {booking.name}',
                f'Message: {msg}\n\nBooking: {booking.date} at {booking.time}',
                booking.email,
                [settings.ADMIN_EMAIL]
            )
            messages.success(request, 'Your reschedule request has been sent.')
            return redirect('bookings:dashboard')
    else:
        form = RescheduleRequestForm()

    return render(request, 'bookings/reschedule_form.html', {'form': form})
