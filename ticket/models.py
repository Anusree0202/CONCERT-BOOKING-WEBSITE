from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now 

class Concert(models.Model):
    name = models.CharField(max_length=500)
    date= models.DateField()
    time = models.TimeField()
    venue = models.CharField(max_length=500)
    ticket_price = models.DecimalField(max_digits=10, decimal_places=2)
    available_tickets = models.IntegerField()

def __str__(self):
        return self.name

class Booking(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, null=False, related_name='ticket_bookings')
    concert = models.ForeignKey(Concert, on_delete=models.CASCADE) 
    user_name = models.CharField(max_length=100)
    tickets_booked = models.PositiveIntegerField()
    booking_date = models.DateTimeField(default=now)
    num_tickets = models.IntegerField(default=1)
 
  

   

