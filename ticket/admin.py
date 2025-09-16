from django.contrib import admin
from .models import Concert, Booking

@admin.register(Concert)
class ConcertAdmin(admin.ModelAdmin):
    list_display = ('name', 'date', 'time', 'venue', 'ticket_price', 'available_tickets')

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('concert', 'user', 'tickets_booked')

