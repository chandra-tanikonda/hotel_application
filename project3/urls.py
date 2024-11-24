from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from hotel_app import views
from hotel_app.views import (
    home_page, signup_view, admin_logout, hotel_admin_login,
    show_admin_profile, update_profile, add_service,
    admin_home, customer_home, hotel_user_profile,
    view_hotel_rooms, reserve_room, select_services, booking_confirmation,
    hotel_payment_info, customer_reservations, service_list, add_new_room, CustomLogoutView,
    update_address, update_payment, update_customer_profile, view_payment_details
)

urlpatterns = [
    # Admin Panel
    path('admin/', admin.site.urls),  # Django admin panel for site management

    # Home Page
    path('', home_page, name='hotel_app_home_page'),  # Home page for the hotel application

    # Authentication & Profile Management
    path('hotel/admin/login/', hotel_admin_login, name='hotel_admin_login'),  # Admin login
    path('hotel/customer/login/', hotel_admin_login, name='customer_login'),  # Customer login
    path('hotel/admin/signup/', signup_view, name='signup'),  # Admin signup
    path('hotel/user/signup/', signup_view, name='user_signup'),  # Customer signup
    path('hotel/admin/logout/', admin_logout, name='admin_logout'),  # Admin logout
    path('logout/', CustomLogoutView, name='logout'),  # General logout for customers and admins

    # Admin Profile & Dashboard
    path('hotel/admin/home/', admin_home, name='admin_user_home'),  # Admin dashboard
    path('hotel/admin/profile/', show_admin_profile, name='admin_profile'),  # View admin profile
    path('hotel/admin/update_profile/', update_profile, name='update_profile'),  # Update admin profile

    # Customer Profile & Dashboard
    path('hotel/customer/home/', customer_home, name='customer_home'),  # Customer dashboard
    path('user/profile/', hotel_user_profile, name='user_profile'),  # View customer profile
    path('update/user/profile/', update_customer_profile, name='update_user_profile'),  # Update customer profile
    path('customer/update/address/', update_address, name='update_address'),  # Update customer address
    path('customer/update_payment/', update_payment, name='update_payment'),  # Update payment details

    # Room Management
    path('hotel/all/rooms/', view_hotel_rooms, name='available_rooms'),  # View all available rooms
    path('hotel/add_room/', add_new_room, name='add_room'),  # Add new room (Admin)

    # Reservation & Booking
    path('hotel/reserve_room/<int:room_id>/', reserve_room, name='reserve_room'),  # Reserve a room
    path('hotel/services/<int:reservation_id>/', select_services, name='select_services'),
    # Add services to a reservation
    path('reservation/confirmation/<int:reservation_id>/', booking_confirmation, name='booking_confirmation'),
    # Booking confirmation page
    path('hotel/customer/bookings/', customer_reservations, name='user_bookings'),  # View customer reservations

    # Payment
    path('hotel/payment/info/<int:reservation_id>/', hotel_payment_info, name='payment_info'),
    # Payment page for reservation
    path('payment/details/', view_payment_details, name='view_payment_details'),  # View customer payment details

    # Services
    path('hotel/add/service/', add_service, name='add_service'),  # Add new service (Admin)
    path('hotel/services/', service_list, name='service_list'),  # View available services

    path('room/<int:room_id>/mark_not_active/', views.mark_room_not_active, name='mark_room_not_active'),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
