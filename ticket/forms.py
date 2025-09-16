from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import Concert
from .models import Booking

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
        return user

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['concert', 'tickets_booked']
    def clean_tickets_booked(self):
        tickets = self.cleaned_data['tickets_booked']
        if tickets > 3:
            raise forms.ValidationError("You can only book up to 3 tickets.")
        return tickets
    
class ConcertUpdateForm(forms.ModelForm):
  class Meta:
        model = Concert
        fields = ['name', 'date', 'time', 'venue', 'ticket_price', 'available_tickets']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Concert Name'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'venue': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Venue'}),
            'ticket_price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ticket Price'}),
            'available_tickets': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Available Tickets'}),
        }

