from django.urls import path
from ticketapi import views



urlpatterns = [
    path('signup/',views.signup,name='signup_api'),
    path('admin_login/', views.admin_login, name='login_api'),  
    path('create_concert/', views.create_concert, name='addconcertapi'),
    path('concert_read/', views.list_concert, name='listconcert'),
    path('<int:pk>/update_concert/', views.update_concert, name='updateconcertapi'),
    path('<int:pk>/delete_concert/', views.delete_concert, name='deleteconcertapi'),
    path('userlogin/', views.user_login, name='user_login'),
    path('concerts/', views.concert_list, name='concert-list'),
    path('book-ticket/', views.book_ticket, name='book_ticket'), 
    path('user-bookings/', views.user_bookings, name='user_bookings'),
    path('admin-bookings/', views.admin_bookings, name='admin-bookings'),
 
]