from django.contrib.auth import login
from django.http import HttpResponseForbidden
from django.shortcuts import render,get_object_or_404

from . import forms


# Create your views here.

def landing_view(request):
    return render(request,'landing_page.html')

from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import CustomerSignupForm

def home_page(request):
    return render(request,'home_page.html')



def signup_view(request):
    """
    Single view to handle both customer and admin sign-up or update processes in one function.
    """
    if request.method == 'POST':
        # Handling POST requests for sign-up or profile update
        mobile_number = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if "update" in request.path:
            # Update the existing user information
            request.user.first_name = first_name
            request.user.last_name = last_name
            request.user.email = email
            request.user.username = mobile_number
            request.user.save()
            user = request.user
        else:
            # Creating a new customer
            user = Customer(
                username=mobile_number,
                mobile_number=mobile_number,
                first_name=first_name,
                last_name=last_name,
                email=email,
            )
            user.set_password(password)
            user.save()
            if "admin" in str(request.path).lower():
                user.is_superuser = True
                user.is_staff = True
            user.save()

            login(request, user)

        # Redirect based on the user role (admin or customer)
        return redirect('admin_user_home' if user.is_superuser else 'customer_home')

    else:
        # Handling GET requests by rendering the sign-up form
        action = (
            "/update/customer/profile/" if "user" in request.path else
            "/update/admin/profile/" if "update" in request.path else
            "/hotel/customer/signup/" if "user" in request.path else
            "/hotel/admin/signup/"
        )
        print(request.path)
        return render(request, 'user_signup.html', {'action': action})
from .forms import UserLoginForm

from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import UserLoginForm  # Ensure this is imported correctly

def hotel_admin_login(request):
    """
    View for handling customer login. Displays the login form on GET requests and authenticates
    the user on POST requests. If login is successful, redirects to the customer's home page.

    Args:
        request: HTTP request object.

    Returns:
        HTTP response: Renders the login form on GET requests or redirects on successful login.
    """
    error_message = ''
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = Customer.objects.filter(username=username).first()

        if user is not None:
            if user:  # Ensure the user is an admin
                login(request, user)
                if "admin" in request.path:
                    return redirect('admin_user_home')
                else:
                    return redirect('customer_home')

            else:
                error_message = "You do not have admin access."
        else:
            error_message = "Invalid username or password."

    # Render the login page with the form (either filled or empty)
    return render(request, 'admin_login.html', {'error_message': error_message})




def administraion_user_home(request):
    print("coming here")
    return render(request,'administraion_user_home.html')


def update_address(request):
    """
    View for handling the update of a customer's address details.
    """
    if request.method == 'POST':
        # Retrieve form data
        address1 = request.POST.get('address1')
        apt_number = request.POST.get('apt_number')
        city = request.POST.get('city')
        state = request.POST.get('state')
        zip_code = request.POST.get('zip_code')

        # Update customer's address information
        customer = request.user
        customer.address1 = address1
        customer.apt_number = apt_number
        customer.city = city
        customer.state = state
        customer.zip_code = zip_code
        customer.save()

        # Success message and redirect
        messages.success(request, "Your address details have been updated successfully.")
        return redirect('update_payment')

    return render(request, 'update_address.html', {'user': request.user})


def update_payment(request):
    """
    View for handling the update of a customer's payment details.
    """
    customer = request.user

    # Retrieve or create a PaymentDetail instance for the logged-in customer
    payment_detail, created = PaymentDetail.objects.get_or_create(customer=customer)

    if request.method == 'POST':
        # Retrieve form data
        name_on_card = request.POST.get('name_on_card')
        card_type = request.POST.get('card_type')
        card_number = request.POST.get('card_number')
        exp_month = request.POST.get('exp_month')
        exp_year = request.POST.get('exp_year')

        # Update payment details
        payment_detail.name_on_card = name_on_card
        payment_detail.card_type = card_type
        payment_detail.card_number = card_number
        payment_detail.exp_month = exp_month
        payment_detail.exp_year = exp_year
        payment_detail.save()

        # Success message and redirect
        messages.success(request, "Your payment details have been updated successfully.")
        return redirect('customer_home')

    return render(request, 'update_payment.html', {'payment_detail': payment_detail})

def admin_home(request):
    return render(request, 'admin_home.html')
def customer_home(request):
    return render(request,'user_home.html')

from .models import Room
from django.shortcuts import render
from .models import Room  # Replace with your actual model import

from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from .models import Room


def mark_room_not_active(request, room_id):
    """
    View to mark a room as not active.

    Args:
        request: The HTTP request object.
        room_id: The ID of the room to mark as not active.

    Returns:
        Redirect to the room list or details page.
    """
    # Get the room object or return 404 if not found
    room = get_object_or_404(Room, pk=room_id)

    # Toggle the mark_not_active field
    room.mark_not_active = True
    room.is_available = False
    room.is_available = False  # Optionally make the room unavailable
    room.save()

    # Add a success message
    messages.success(request, f"Room {room.room_num} has been marked as not active.")

    # Redirect to a relevant page (e.g., room list or room details)
    return redirect('available_rooms')  # Replace 'room_list' with the actual name of your view


def view_hotel_rooms(request):
    """
    View for displaying a list of hotel rooms based on search criteria.
    """
    query_params = get_query_params(request)
    filtered_rooms = filter_rooms(**query_params)

    context = {
        'rooms': filtered_rooms,
        'min_price_per_night': query_params.get('min_price_per_night', ''),
        'max_price_per_night': query_params.get('max_price_per_night', '')
    }
    return render(request, 'available_rooms.html', context)

def get_query_params(request):
    """
    Extracts and returns the query parameters for room filtering.
    """
    return {
        'query': request.GET.get('q', ''),
        'room_type': request.GET.get('type', ''),
        'min_price_per_night': request.GET.get('min_price_per_night', ''),
        'max_price_per_night': request.GET.get('max_price_per_night', '')
    }

def filter_rooms(query='', room_type='', min_price_per_night='', max_price_per_night=''):
    """
    Filters and returns rooms based on the provided search criteria.
    """
    rooms = Room.objects.all()

    if query:
        rooms = rooms.filter(number__icontains=query)
    if room_type:
        rooms = rooms.filter(room_type=room_type)
    if min_price_per_night:
        rooms = rooms.filter(price_per_night__gte=min_price_per_night)
    if max_price_per_night:
        rooms = rooms.filter(price_per_night__lte=max_price_per_night)

    return rooms



from .forms import BookingForm



from django.shortcuts import render, redirect, get_object_or_404
from .models import Room  # Ensure correct import
from .forms import BookingForm  # Ensure correct import

def reserve_room(request, room_id):
    """
    View for handling room booking, displaying the booking form on GET requests
    and processing the booking on POST requests.

    Args:
        request: The HTTP request object.
        room_id: The ID of the room to be booked.

    Returns:
        Renders the booking form template on GET requests or redirects
        to the service selection page on successful booking.
    """
    # Retrieve the room instance or return 404 if not found
    room = get_object_or_404(Room, pk=room_id)

    if request.method == 'POST':
        # Handle the booking submission
        form = BookingForm(request.POST)
        if form.is_valid():
            # Create the booking and associate it with the room and user
            booking = form.save(commit=False)
            booking.room = room
            booking.customer = request.user
            booking.save()

            # Update the room's availability to 'Unavailable'
            room.is_available = False
            room.save()

            # Redirect to the service selection page for the booking
            return redirect('select_services', reservation_id=booking.id)
    else:
        # Render the booking form for GET requests
        form = BookingForm()

    return render(request, 'hotel_book_room.html', {'form': form, 'room': room})

def create_booking_from_form(form, room, user):
    """
    Creates a booking instance from the form, without saving to the database.
    """
    booking = form.save(commit=False)
    booking.room = room
    booking.customer = user
    booking.total_cost = room.rate_per_night  # Modify if calculation is needed
    booking.save()
    return booking

def update_room_availability(room, is_available):
    """
    Updates the availability of the room.
    """
    room.is_available = is_available
    room.save()




from .forms import ServiceForm

from .models import Reservation,ReservationService

from django.shortcuts import render, redirect, get_object_or_404
from .models import Reservation, ReservationService  # Ensure correct import
from .forms import ServiceForm  # Ensure correct import


def select_services(request, reservation_id):
    """
    View for selecting additional services for a reservation.
    """
    booking = get_object_or_404(Reservation, pk=reservation_id)

    if request.method == 'POST':
        form = ServiceForm(request.POST)
        if form.is_valid():
            # Remove any existing services for this reservation to avoid duplicates
            ReservationService.objects.filter(reservation=booking).delete()

            # Add new services to the booking through ReservationService
            for service in form.cleaned_data['services']:
                ReservationService.objects.create(
                    reservation=booking,
                    extra_service=service,
                    count=1  # Set default quantity, or add another form field for this if needed
                )
            return redirect('booking_confirmation', reservation_id=booking.id)
    else:
        form = ServiceForm()

    return render(request, 'select_services.html', {'form': form, 'booking': booking})

def add_services_to_booking(form, booking):
    """
    Adds selected services to the booking.
    """
    selected_services = form.cleaned_data['services']
    for service in selected_services:
        ReservationService.objects.create(
            reservation=booking,
            extra_service=service,
            count=1
        )





from django.shortcuts import render, get_object_or_404
from .models import Reservation, ReservationService  # Ensure correct import

def booking_confirmation(request, reservation_id):
    """
    View for displaying the booking confirmation details.
    """
    booking = get_booking_or_404(reservation_id)
    print("price per night")
    print(booking.room.price_per_night)
    booking_services = get_booking_services(booking)
    total_cost = calculate_total_cost(booking)
    print("total_cost")
    print(total_cost)
    context = {
        'booking': booking,
        'booking_services': booking_services,
        'total_cost': total_cost,
    }

    return render(request, 'booking_confirmation.html', context)

def get_booking_or_404(reservation_id):
    """
    Retrieves the booking instance or returns a 404 error if not found.
    """
    return get_object_or_404(Reservation, id=reservation_id)

def get_booking_services(reservation):
    """
    Retrieves services associated with the booking.
    """
    return ReservationService.objects.filter(reservation=reservation)


def calculate_total_booking_cost(booking, associated_services):
    """
    Calculates the total cost of a booking, including the cost of associated additional services.

    Args:
        booking: The booking object for which the total cost is being calculated.
        associated_services: A queryset or list of associated service objects for the booking.

    Returns:
        The total cost as a sum of the booking's base price and the price of all additional services.
    """
    # Calculate the total cost for all additional services
    total_services_cost = sum(service.extra_service.rate_per_night * service.count
                              for service in associated_services)

    # Calculate and return the total booking cost
    total_booking_cost = booking.total_cost + total_services_cost
    return total_booking_cost


from django.utils import timezone
from .forms import CreditCardForm
from .models import Reservation, ReservationService, Room, PaymentDetail,PaymentTransaction

from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from .models import Reservation, ReservationService, PaymentTransaction  # Make sure these are correctly imported
from .forms import CreditCardForm  # Make sure this is correctly imported


def hotel_payment_info(request, reservation_id):
    """
    Handles the payment process for a hotel booking.
    If a saved payment method exists, it will use that; otherwise, it will prompt for payment details.
    """
    booking = get_object_or_404(Reservation, pk=reservation_id)
    total_cost = calculate_total_cost(booking)

    # Check if the user has a saved payment method
    latest_payment_method = PaymentDetail.objects.filter(customer=request.user).order_by('-created_at').first()

    if request.method == 'POST':
        # If there is a saved payment method, proceed with it
        if latest_payment_method:
            return process_payment_with_saved_method(request, booking, total_cost, latest_payment_method)
        else:
            return process_new_payment(request, booking, total_cost)
    else:
        if latest_payment_method:
            return process_payment_with_saved_method(request, booking, total_cost, latest_payment_method)
        # Render payment form if no saved payment method
        return render_payment_form(request, booking, total_cost, latest_payment_method)


def render_payment_form(request, booking, total_cost, latest_payment_method=None):
    """
    Renders the payment form if no saved method is found, otherwise displays the saved method.
    """
    if latest_payment_method:
        # Show summary of saved payment method and allow customer to proceed
        return render(request, 'confirm_saved_payment.html', {
            'booking': booking,
            'total_cost': total_cost,
            'payment_method': latest_payment_method
        })
    else:
        # Show new payment form
        form = CreditCardForm()
        return render(request, 'credit_card_info.html', {'form': form, 'booking': booking, 'total_cost': total_cost})


def process_payment_with_saved_method(request, booking, total_cost, payment_method):
    """
    Processes payment using the latest saved payment method.
    """
    update_booking_and_room_status(booking)
    create_transaction_record(booking, total_cost, payment_method)
    send_booking_confirmation_email(booking, total_cost)
    return redirect('user_bookings')


def process_new_payment(request, booking, total_cost):
    """
    Processes new payment details entered by the user.
    """
    form = CreditCardForm(request.POST)
    if form.is_valid():
        # Save new payment method details
        payment_detail = form.save(commit=False)
        payment_detail.customer = request.user
        payment_detail.save()

        # Complete the payment process
        update_booking_and_room_status(booking)
        create_transaction_record(booking, total_cost, payment_detail)
        send_booking_confirmation_email(booking, total_cost)
        return redirect('customer_home')

    return render(request, 'credit_card_info.html', {'form': form, 'booking': booking, 'total_cost': total_cost})


def render_payment_form(request, booking, total_cost):
    """
    Renders the payment form for GET requests.
    """
    form = CreditCardForm()
    return render(request, 'credit_card_info.html', {'form': form, 'booking': booking, 'total_cost': total_cost})
def process_payment(request, booking, total_cost):
    """
    Processes the payment form submission.
    """
    form = CreditCardForm(request.POST)
    if form.is_valid():
        credit_card = (form, request.user)
        update_booking_and_room_status(booking)
        create_transaction_record(booking, total_cost, credit_card)
        send_booking_confirmation_email(booking,total_cost)
        return redirect('customer_home')

    return render(request, 'credit_card_info.html', {'form': form, 'booking': booking, 'total_cost': total_cost})

def get_booking_or_404(reservation_id):
    """
    Retrieves the booking instance or returns a 404 error if not found.
    """
    return get_object_or_404(Reservation, id=reservation_id)

from decimal import Decimal

def calculate_total_cost(booking):
    """
    Calculates the total cost of the booking including additional services.
    """
    # Calculate the additional services cost
    additional_services_cost = sum(
        bs.extra_service.rate_per_night * bs.count
        for bs in ReservationService.objects.filter(reservation=booking)
    )

    # Ensure total_cost is not None
    total_cost = booking.room.price_per_night if booking.room.price_per_night is not None else Decimal(0)

    return total_cost + additional_services_cost




def save_credit_card_info(form, user):
    """
    Saves the credit card information from the form.
    """
    credit_card = form.save(commit=False)
    credit_card.customer = user
    credit_card.save()
    return credit_card


def update_booking_and_room_status(booking):
    """
    Updates the booking status and the availability of the associated room.
    """
    booking.is_active = True
    booking.room.is_available = False
    booking.save()

from django.contrib.auth import logout

def CustomLogoutView(request):
    logout(request)
    return redirect('customer_login')


def create_transaction_record(booking, total_cost, credit_card):
    """
    Creates a transaction record for the booking payment.
    """
    try:
        PaymentTransaction.objects.create(
            reservation=booking,
            paid_amount=total_cost,
            payment_information=credit_card,
            method='credit-card',
            transaction_date=timezone.now(),
            transaction_status='completed'
        )
        booking.is_active = True
        booking.save()
    except Exception as e:
        print("Exception in creating the payment:", str(e))


def send_booking_confirmation_email(booking,total_cost):
    """
    Sends a confirmation email for the booking.
    """
    try:
        # Replace this with your actual email sending function
        send_booking_receipt_email(booking,total_cost)
    except Exception as e:
        print("Error in sending mail:", str(e))





def user_bookings(request):
    user = request.user
    bookings = PaymentTransaction.objects.filter(booking__user=user)
    print("bookings",bookings)
    return render(request, 'user_bookings.html', {'bookings': bookings})


# views.py

from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings

def send_booking_receipt_email(booking,total_cost):
    subject = 'Your Hotel Reservation Receipt'
    html_message = render_to_string('email_receipt.html', {'booking': booking,'total_cost':total_cost})
    plain_message = strip_tags(html_message)
    from_email = settings.DEFAULT_FROM_EMAIL
    to = booking.customer.email

    send_mail(subject, plain_message, from_email, [to], html_message=html_message)

def print_receipt(request, reservation_id):
    booking = get_object_or_404(Reservation, id=reservation_id)
    # Make sure the customer requesting the receipt is the one who made the booking
    if request.user != booking.customer:
        return HttpResponseForbidden()
    return render(request, 'print_receipt.html', {'booking': booking})


from .forms import RoomForm

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import RoomForm  # Make sure this import is correct


@login_required
def add_new_room(request):
    """
    View for adding a new room. Restricted to staff members only.
    """
    if request.method == 'POST':
        room_num = request.POST.get('room_num')
        room_type = request.POST.get('room_type')
        room_capacity = request.POST.get('room_capacity')
        price_per_night = request.POST.get('price_per_night')
        is_available = 'is_available' in request.POST
        details = request.POST.get('details')
        image = request.FILES.get('image')

        # Create the Room instance and save it
        Room.objects.create(
            room_num=room_num,
            room_type=room_type,
            room_capacity=room_capacity,
            price_per_night=price_per_night,
            is_available=is_available,
            details=details,
            image=image
        )

        return redirect('available_rooms')  # Redirect to room listing or confirmation page after saving

    return render(request, 'add_room.html')

from .forms import AddServiceForm

def add_service(request):
    if request.method == 'POST':
        service_name = request.POST.get('service_name')
        price_per_night = request.POST.get('price_per_night')
        description = request.POST.get('description')

        # Validate and save the new service entry
        if service_name and price_per_night:
            service = Services(
                name=service_name,
                rate_per_night=price_per_night,
                service_details=description
            )
            service.save()

            return redirect('service_list')  # Redirect to the service list view
    return render(request, 'add_new_service.html')

from .models import Services
def service_list(request):
    """
        View function to display a list of all available extra services.

        Args:
            request: The HTTP request object.

        Returns:
            HTTP response with rendered template.
    """
    services = Services.objects.all()
    return render(request, 'service_list.html', {'services': services})

from .models import Customer
def get_all_customers_info(request):
    users = Customer.objects.filter(is_superuser=False)
    return render(request,'users_list.html',{'users':users})

@login_required
def update_profile(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone_number = request.POST.get('username')

        # Update the admin profile
        user = request.user
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.username = phone_number  # Assuming 'username' field is used for phone number
        user.save()


        return redirect('admin_profile')

    return render(request, 'admin_update_profile.html', {
        'user': request.user
    })
def hotel_user_profile(request):
    if request.user.is_active:
        print("activa customer")
    else:
        print("no active customer")
    return render(request, 'user_profile.html')

from .forms import UpdateProfileForm

def update_customer_profile(request):
    """
    View to allow customers to update their profile details.
    """
    if request.method == 'POST':
        form = UpdateProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            #messages.success(request, 'Your profile has been updated successfully.')
            return redirect('user_profile')
    else:
        form = UpdateProfileForm(instance=request.user)

    context = {
        'form': form,
    }
    return render(request, 'update_profile.html', context)

def view_payment_details(request):
    """
    View to display the payment details of the logged-in customer.
    """
    payment_details = PaymentDetail.objects.filter(customer=request.user)
    return render(request, 'view_payment_details.html', {'payment_details': payment_details})

def show_admin_profile(request):
    if request.user.is_active:
        print("activa customer")
    else:
        print("no active customer")
    return render(request, 'admin_profile.html')

def reservations_list(request):
    bookings = Reservation.objects.all()
    return render(request, 'bookings_list.html', {'bookings': bookings})

# views.py


def get_bookings_with_services(user, is_admin=False):
    """
    Retrieve all bookings with service details and calculate total costs.
    If user is an admin, return all bookings; otherwise, return only customer-specific bookings.
    """
    # Retrieve all bookings if the user is an admin; otherwise, filter by the logged-in customer.
    bookings = Reservation.objects.all() if is_admin else Reservation.objects.filter(customer=user)

    bookings_with_services = []

    for booking in bookings:
        # Calculate the total nights for the stay
        total_nights = 1

        # Calculate room cost
        room_cost = booking.room.price_per_night * total_nights if booking.room else Decimal(0)

        # Calculate additional services cost
        booking_services = booking.reservation_services.all()
        total_service_cost = sum(service.extra_service.rate_per_night * service.count for service in booking_services)

        # Calculate grand total (room cost + additional services cost)
        grand_total = room_cost + total_service_cost

        # Append booking details
        bookings_with_services.append({
            'booking': booking,
            'booking_services': booking_services,
            'total_service_cost': total_service_cost,
            'grand_total': grand_total
        })

    return bookings_with_services

from django.contrib import messages
def admin_logout(request):
    """
    Logs out the admin user and redirects to the login page.
    """
    if request.user.is_authenticated and request.user.is_staff:
        logout(request)
        messages.success(request, "You have successfully logged out.")
    return redirect('hotel_admin_login')  # Replace 'login' with your login URL name

def customer_reservations(request):
    """
    View to display all bookings for the logged-in user. If the user is an admin, display all reservations.
    """
    is_admin = request.user.is_staff  # Check if the user is an admin
    bookings_with_services = get_bookings_with_services(request.user, is_admin=is_admin)
    return render(request, 'reservations.html', {'bookings_with_services': bookings_with_services})



