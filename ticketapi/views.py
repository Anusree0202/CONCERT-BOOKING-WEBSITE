from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.views.decorators.csrf import csrf_exempt
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from ticketapi.serializers import AdminBookingSerializer, concertSerializer
from ticketapi.models import Concert,Booking
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import User
from rest_framework.permissions import IsAdminUser

@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    username = request.data.get("username", "").strip()  
    email = request.data.get("email", "").strip()
    password1 = request.data.get("password1")
    password2 = request.data.get("password2")

    if not username or not email or not password1 or not password2:
        return Response({'error': 'All fields are required!'}, status=status.HTTP_400_BAD_REQUEST)


    if password1 != password2:
        return Response({'error': 'Passwords do not match!'}, status=status.HTTP_400_BAD_REQUEST)

    if User.objects.filter(username=username).exists():
        return Response({'error': 'Username already taken!'}, status=status.HTTP_400_BAD_REQUEST)

    if User.objects.filter(email=email).exists():
        return Response({'error': 'Email already registered!'}, status=status.HTTP_400_BAD_REQUEST)

    user = User.objects.create_user(username=username, email=email, password=password1)
    token, _ = Token.objects.get_or_create(user=user)

    return Response({'message': 'Account created successfully!', 'token': token.key}, status=status.HTTP_201_CREATED)

@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])  
def admin_login(request):
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(username=username, password=password)

    if user is not None:
        if user.is_staff:  # Ensure only admins can log in
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key, 'message': 'Admin login successful'})
        else:
            return Response({'error': 'Access denied. Only admins can log in.'}, status=403)
    return Response({'error': 'Invalid username or password.'}, status=401)



from ticket.forms import ConcertUpdateForm
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_concert(request):
    serializer = concertSerializer(data=request.data)
    if serializer.is_valid():
        concert = serializer.save()
        return Response({'id': concert.id}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes((AllowAny,))
def list_concert(request):
    concerts = Concert.objects.all().values()
    return JsonResponse(list(concerts), safe=False)

@api_view(['PUT'])
@permission_classes((AllowAny,))
def update_concert(request, pk):
    product = get_object_or_404(Concert, pk=pk)
    form = ConcertUpdateForm(request.data, instance=product)
    if form.is_valid():
        form.save()
        serializer = concertSerializer(product)
        return Response(serializer.data)
    else:
        return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['DELETE'])
@permission_classes((AllowAny,))
def delete_concert(request, pk):
    try:
        concert = Concert.objects.get(pk=pk)  
    except concert.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    concert.delete()
    return Response("deleted successfully")


@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def user_login(request):
    print("Received data:", request.data)

    username = request.data.get('username')
    password = request.data.get('password')

    if not username or not password:
        return Response({"error": "Username and password are required."}, status=400)

    user = authenticate(username=username, password=password)

    if user is not None:
        token, created = Token.objects.get_or_create(user=user)
        return Response({"token": token.key, "message": "User login successful"})
    else:
        return Response({"error": "Invalid username or password."}, status=400)


@api_view(['GET'])
@permission_classes([AllowAny])  # Allow anyone to view the concert list
def concert_list(request):
    """
    API view to retrieve the list of available concerts.
    """
    concerts = Concert.objects.all()
    serializer = concertSerializer(concerts, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def book_ticket(request):
    try:
        user = request.user
        concert_id = request.data.get('concert_id')
        num_tickets = request.data.get('num_tickets')

        if not concert_id or not num_tickets:
            return Response({"error": "Missing concert_id or num_tickets"}, status=400)

        num_tickets = int(num_tickets)
        if num_tickets <= 0:
            return Response({"error": "Number of tickets must be at least 1"}, status=400)

        if num_tickets > 3:
            return Response({"error": "You can book a maximum of 3 tickets only."}, status=400)

        concert = get_object_or_404(Concert, id=concert_id)

        if concert.available_tickets < num_tickets:
            return Response({"error": "Not enough tickets available!"}, status=400)

        concert.available_tickets -= num_tickets
        concert.save()

        booking = Booking.objects.create(
            user=user,
            concert=concert,
            user_name=user.username,
            tickets_booked=num_tickets
        )

        return Response({
            "message": "Tickets booked successfully!",
            "booking_id": booking.id,
            "concert": concert.name,
            "tickets_booked": num_tickets,
            "remaining_tickets": concert.available_tickets
        }, status=201)

    except Exception as e:
        return Response({"error": str(e)}, status=500)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_bookings(request):
    """
    API view to retrieve bookings made by the logged-in user.
    """
    try:
        user = request.user
        bookings = Booking.objects.filter(user=user).select_related('concert')

        data = [
            {
                "booking_id": booking.id,
                "concert_name": booking.concert.name,
                "concert_date": booking.concert.date,
                "venue": booking.concert.venue,
                "tickets_booked": booking.tickets_booked
            }
            for booking in bookings
        ]

        return Response(data, status=status.HTTP_200_OK)

    except Exception as e:
        return Response(
            {"error": "An error occurred while fetching bookings."},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def admin_bookings(request):
    if not request.user.is_staff:
     return Response({"error": "You are not authorized to view this."}, status=403)


    bookings = Booking.objects.select_related('concert', 'user').all().order_by('-booking_date')

    data = []
    for booking in bookings:
        data.append({
            "user_name": booking.user.username,
            "concert_name": booking.concert.name,
            "tickets_booked": booking.tickets_booked,
            "booking_date": booking.booking_date.strftime("%Y-%m-%d %H:%M:%S"),
        })

    return Response(data, status=status.HTTP_200_OK)


    









