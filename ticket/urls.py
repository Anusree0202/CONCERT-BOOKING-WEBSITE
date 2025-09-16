from django.urls import path
from . import views
from django.contrib.auth import views as auth_views



urlpatterns = [
    path('', views.home, name='home'),
    path('concerts/', views.concert_list, name='concert_list'),
    path('signup/',views.signup,name='signup'),
    path('userlogin/',views.login_page,name='userlogin'),
    path('book/<int:concert_id>/', views.book_ticket, name='book_ticket'),
    path('admin-login/', views.admin_login, name='admin_login'),
    path('add_concert/', views.add_concert, name='add_concert'),
    path('concert_read/', views.concert_read, name='concert_read'),
    path('concert_read/<int:pk>/edit/', views.concert_update, name='concert_update'),
    path('concert_read/<int:pk>/delete/', views.concert_delete, name='concert_delete'),
    path('userlogout/', views.userlogout_view,name='userlogout'),
    path('adminlogout/', views.adminlogout_view,name='adminlogout'),
    path('bookings/', views.admin_booking_list, name='admin_booking_list'),
    path('my-bookings/', views.user_bookings, name='user_bookings'),
    path('delete-booking/<int:booking_id>/', views.delete_booking, name='delete_booking'),
    
    
]

