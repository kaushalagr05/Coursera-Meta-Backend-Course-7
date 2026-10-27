import json
from datetime import datetime
from django.shortcuts import render
from django.http import HttpResponse
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from .models import Booking, Menu
from .forms import BookingForm


def home(request):
    """Render home page."""
    return render(request, 'index.html')


def about(request):
    """Render about page."""
    return render(request, 'about.html')


def menu(request):
    """Render menu listing page."""
    menu_data = Menu.objects.all()
    main_data = {"menu": menu_data}
    return render(request, 'menu.html', main_data)


def display_menu_items(request, pk=None):
    """Render single menu item detail."""
    if pk:
        menu_item = Menu.objects.get(pk=pk)
    else:
        menu_item = ""
    return render(request, 'menu_item.html', {"menu_item": menu_item})


def book(request):
    """Render booking form page."""
    form = BookingForm()
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            form.save()
    context = {'form': form}
    return render(request, 'book.html', context)


def reservations(request):
    """Render reservations listing page with serialized JSON."""
    date = request.GET.get('date', datetime.today().date())
    bookings = Booking.objects.all()
    booking_json = serializers.serialize('json', bookings)
    return render(request, 'reservations.html', {'bookings': booking_json})


@csrf_exempt
def bookings(request):
    """API endpoint for fetching bookings by date (GET) and creating reservations (POST)."""
    if request.method == 'POST':
        data = json.loads(request.body)
        exist = Booking.objects.filter(
            reservation_date=data['reservation_date'],
            reservation_slot=data['reservation_slot']
        ).exists()

        if not exist:
            booking = Booking(
                first_name=data['first_name'],
                reservation_date=data['reservation_date'],
                reservation_slot=data['reservation_slot'],
            )
            booking.save()
            return HttpResponse(
                json.dumps({'status': 1, 'message': 'Reservation successful'}),
                content_type='application/json',
                status=201
            )
        else:
            return HttpResponse(
                json.dumps({'error': 1, 'message': 'Slot already booked'}),
                content_type='application/json',
                status=400
            )

    # Handle GET request: filter by date or default to today's date
    date = request.GET.get('date', datetime.today().date())
    bookings = Booking.objects.filter(reservation_date=date)
    booking_json = serializers.serialize('json', bookings)
    return HttpResponse(booking_json, content_type='application/json')
