from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now 

class Concert(models.Model):
    name = models.CharField(max_length=100)
    date = models.DateField()
    time = models.TimeField()
    venue = models.CharField(max_length=200)
    ticket_price = models.DecimalField(max_digits=8, decimal_places=2)
    available_tickets = models.PositiveIntegerField()

    def __str__(self):
        return self.name


class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    concert = models.ForeignKey(Concert, on_delete=models.CASCADE)  # ✅ using ticketapi_concert
    user_name = models.CharField(max_length=100)
    tickets_booked = models.PositiveIntegerField()
    booking_date = models.DateTimeField(default=now)

    def __str__(self):
        return f"{self.user_name} - {self.concert.name}"


