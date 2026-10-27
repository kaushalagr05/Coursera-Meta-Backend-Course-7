import json
from datetime import date
from django.test import TestCase, Client
from django.urls import reverse
from restaurant.models import Booking, Menu
from restaurant.forms import BookingForm


class BookingModelTest(TestCase):
    """Test Booking model fields and string representation."""

    def setUp(self):
        self.booking = Booking.objects.create(
            first_name="John Doe",
            reservation_date=date(2026, 11, 15),
            reservation_slot=14
        )

    def test_booking_creation(self):
        self.assertEqual(self.booking.first_name, "John Doe")
        self.assertEqual(self.booking.reservation_date, date(2026, 11, 15))
        self.assertEqual(self.booking.reservation_slot, 14)

    def test_booking_str_representation(self):
        self.assertEqual(str(self.booking), "John Doe - 2026-11-15 14:00")


class BookingFormTest(TestCase):
    """Test BookingForm validation."""

    def test_valid_form(self):
        form = BookingForm(data={
            'first_name': 'Jane Doe',
            'reservation_date': '2026-11-16',
            'reservation_slot': 12
        })
        self.assertTrue(form.is_valid())


class BookingViewsTest(TestCase):
    """Test URL routes, rendering, and API endpoints."""

    def setUp(self):
        self.client = Client()
        self.today = date.today()
        self.booking_today = Booking.objects.create(
            first_name="Alice",
            reservation_date=self.today,
            reservation_slot=11
        )
        self.booking_future = Booking.objects.create(
            first_name="Bob",
            reservation_date=date(2026, 12, 25),
            reservation_slot=18
        )

    def test_book_view(self):
        response = self.client.get(reverse('book'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'book.html')
        self.assertIn('form', response.context)

    def test_reservations_view(self):
        response = self.client.get(reverse('reservations'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'reservations.html')
        self.assertIn('bookings', response.context)
        # Check that serialized JSON contains our bookings
        self.assertIn("Alice", response.context['bookings'])
        self.assertIn("Bob", response.context['bookings'])

    def test_bookings_get_default_today(self):
        response = self.client.get(reverse('bookings'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')
        data = json.loads(response.content)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['fields']['first_name'], 'Alice')
        self.assertEqual(data[0]['fields']['reservation_slot'], 11)

    def test_bookings_get_specific_date(self):
        response = self.client.get(f"{reverse('bookings')}?date=2026-12-25")
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['fields']['first_name'], 'Bob')
        self.assertEqual(data[0]['fields']['reservation_slot'], 18)

    def test_bookings_post_success(self):
        payload = {
            'first_name': 'Charlie',
            'reservation_date': '2026-12-25',
            'reservation_slot': 12
        }
        response = self.client.post(
            reverse('bookings'),
            data=json.dumps(payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 201)
        self.assertTrue(Booking.objects.filter(first_name='Charlie', reservation_slot=12).exists())

    def test_bookings_post_duplicate_rejection(self):
        # Bob already booked 2026-12-25 at slot 18
        payload = {
            'first_name': 'David',
            'reservation_date': '2026-12-25',
            'reservation_slot': 18
        }
        response = self.client.post(
            reverse('bookings'),
            data=json.dumps(payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.content)
        self.assertEqual(data.get('error'), 1)
