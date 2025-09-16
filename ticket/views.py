from pyexpat.errors import messages
from django.shortcuts import render, get_object_or_404, redirect
from ticketapi.models import Concert,Booking
from django.shortcuts import render,redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login 
from .forms import ConcertUpdateForm, CustomUserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib import messages
from ticketapi import models



def home(request):
    concerts = Concert.objects.all() 
    return render(request, 'home.html', {'concerts': concerts})


def concert_list(request):
    concerts = Concert.objects.all()  
    return render(request, 'concert_list.html', {'concerts': concerts})


def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()  
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'signup.html', {'form': form})


def login_page(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('concert_list')
    else:
        form = AuthenticationForm()
    return render(request, 'userlogin.html', {'form': form})


@login_required(login_url='/userlogin/')
def userlogout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')
    context = {
        'user': request.user
    }
    return render(request, 'userlogout.html', context)



@login_required
def book_ticket(request, concert_id):
    concert = get_object_or_404(Concert, id=concert_id)

    if request.method == "POST":
        tickets_booked = int(request.POST.get('tickets', 0))

        if tickets_booked > 3:
            messages.error(request, "You cannot book more than 3 tickets.")
            return redirect('book_ticket', concert_id=concert.id)

        if tickets_booked > concert.available_tickets:
            messages.error(request, "Not enough tickets available.")
            return redirect('book_ticket', concert_id=concert.id)

        # ✅ **Fix: Save the logged-in user in Booking**
        Booking.objects.create(
            concert=concert,
            user=request.user,  # This ensures user_id is saved
            tickets_booked=tickets_booked
        )

        concert.available_tickets -= tickets_booked
        concert.save()
        messages.success(request, "Tickets booked successfully!")

    return render(request, 'book_ticket.html', {'concert': concert})
    

@login_required
def add_concert(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        date = request.POST.get('date')
        time = request.POST.get('time')
        venue = request.POST.get('venue')
        ticket_price = request.POST.get('ticket_price')
        available_tickets = request.POST.get('available_tickets')
        if not name or not date or not time or not venue or not ticket_price or not available_tickets:
            messages.error(request, "All fields are required.")
        else: 
            Concert.objects.create(
                name=name,
                date=date,
                time=time,
                venue=venue,
                ticket_price=ticket_price,
                available_tickets=int(available_tickets)
            )
            messages.success(request, "Concert added successfully!")
            return redirect('add_concert')
    return render(request, 'add_concert.html')


def admin_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_staff: 
            login(request, user)
            return redirect('concert_read')  
        else:
            messages.error(request, 'Invalid credentials or not an admin.')
    return render(request, 'admin_login.html')


@login_required(login_url='/admin_login/')
def adminlogout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')
    context = {
        'user': request.user
    }
    return render(request, 'adminlogout.html', context)


def concert_read(request):
    concerts = Concert.objects.all()
    return render(request, 'concert_read.html', {'concerts': concerts})


def concert_update(request, pk):
    concert_instance = get_object_or_404(Concert, pk=pk) 
    if request.method == 'POST':
        form =ConcertUpdateForm(request.POST, instance=concert_instance)
        if form.is_valid():
            form.save()
            return redirect('concert_read')  
    else:
        form = ConcertUpdateForm(instance=concert_instance)  
    return render(request, 'update_concert.html', {'form': form, 'concert': concert_instance})


def concert_delete(request, pk):
    concert_instance = get_object_or_404(Concert, pk=pk)  
    if request.method == 'POST':
        concert_instance.delete()
        return redirect('concert_read')  
    return render(request, 'delete_concert.html', {'concert': concert_instance})


def admin_booking_list(request):
    bookings = Booking.objects.all()
    return render(request, 'booking_list.html', {'bookings': bookings})


@login_required
def user_bookings(request):
    bookings = Booking.objects.filter(user=request.user)
    return render(request, 'user_bookings.html', {'bookings': bookings})


def delete_booking(request, booking_id):
    booking = Booking.objects.get(id=booking_id)
    if booking.user == request.user:
        booking.delete()
    return redirect('user_bookings')






