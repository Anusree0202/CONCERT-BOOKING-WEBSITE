from rest_framework import serializers
from ticketapi.models import Concert, Booking

class concertSerializer(serializers.ModelSerializer):
    class Meta:
        model = Concert
        fields = "__all__"

class AdminBookingSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.username', read_only=True)
    concert_name = serializers.CharField(source='concert.name', read_only=True)

    class Meta:
        model = Booking
        fields = ['user_name', 'concert_name', 'tickets_booked', 'booking_date']



