# importing the django default packages
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone



# Custom Customer model that extends AbstractUser
class Customer(AbstractUser):
    first_name = models.CharField(max_length=60, null=True)  # Customer's first name
    last_name = models.CharField(max_length=30, null=True)  # Customer's last name
    email = models.CharField(max_length=100, null=True)  # Customer's email address
    mobile_number = models.CharField(max_length=12, null=True)  # Customer's contact room_num
    address1 = models.CharField(max_length=255, blank=True)  # Street address, e.g., "123 Main St"
    apt_number = models.CharField(max_length=10, blank=True, null=True)  # Apartment or unit number
    city = models.CharField(max_length=100, blank=True)  # City of residence
    state = models.CharField(max_length=50, blank=True)  # State of residence
    zip_code = models.CharField(max_length=10, blank=True)  # ZIP or postal code
    created_at = models.DateTimeField(default=timezone.now)  # Date and time when the profile was created
    updated_at = models.DateTimeField(auto_now=True)  # Date and time when the profile was last modified

    def __str__(self):
        """
        Returns a string representation of the customer, showing their username and email for easy identification.
        """
        return f"{self.username} ({self.email})"

    def get_full_name(self):
        """
        Returns the full name of the customer by combining first and last names.

        Returns:
            str: Customer's full name.
        """
        return f"{self.first_name} {self.last_name}".strip()

    def update_contact_info(self, new_mobile_number=None, new_address=None):
        """
        Updates the customer's contact information, including mobile room_num and address.

        Args:
            new_mobile_number (str): New mobile room_num to update.
            new_address (str): New address to update.

        Returns:
            str: Confirmation message indicating updated fields.
        """
        if new_mobile_number:
            self.mobile_number = new_mobile_number
        if new_address:
            self.address = new_address
        self.save()
        return "Contact information updated successfully."

    def has_recent_activity(self, days=30):
        """
        Checks if the customer has updated their profile within a specified room_num of days.

        Args:
            days (int): Number of days to check for recent activity (default is 30).

        Returns:
            bool: True if the profile was updated within the specified room_num of days, else False.
        """
        return (timezone.now() - self.updated_at).days <= days

# Room
class Room(models.Model):
    HOTEL_ROOM_CHOICES = (
        ('SQN', 'Single Queen'),
        ('SKN', 'Single King'),
        ('DQN', 'Double Queen'),
        ('DKN', 'Double King'),
        ('SKS', 'Suite King'),
    )

    room_num = models.CharField(max_length=5, unique=True)  # Unique room number identifier
    room_type = models.CharField(max_length=3, choices=HOTEL_ROOM_CHOICES)  # Type of room, e.g., Single Queen
    room_capacity = models.IntegerField(null=True)  # Maximum number of occupants for the room
    price_per_night = models.DecimalField(max_digits=6, decimal_places=2)  # Nightly rate for the room
    is_available = models.BooleanField(default=True)  # Availability status of the room
    image = models.ImageField(upload_to='room_images/', null=True, blank=True)  # Image of the room
    details = models.TextField(null=True, blank=True)  # Additional room details, if any
    mark_not_active = models.BooleanField(default=False)
    def __str__(self):
        """
        Returns a string representation of the room, including room number and type for easy identification.
        """
        return f"Room {self.room_num} - {self.get_room_type_display()}"

    def get_room_type_description(self):
        """
        Returns a detailed description of the room type.

        Returns:
            str: A descriptive text for the room type.
        """
        return self.HOTEL_ROOM_CHOICES.get(self.room_type, "Description not available for this room type.")

    def toggle_availability(self):
        """
        Toggles the availability status of the room.

        Returns:
            bool: The updated availability status.
        """
        self.is_available = not self.is_available
        self.save()
        return self.is_available

    def calculate_total_price(self, num_nights):
        """
        Calculates the total cost for a stay based on the number of nights.

        Args:
            num_nights (int): Number of nights for the reservation.

        Returns:
            Decimal: Total price for the specified number of nights.
        """
        return self.price_per_night * num_nights



# Services
class Services(models.Model):
    name = models.CharField(max_length=100)  # Name of the service, e.g., "Jacuzzi", "Extra Bed"
    rate_per_night = models.DecimalField(max_digits=6, decimal_places=2)  # Cost per night for the service
    created_at = models.DateTimeField(default=timezone.now)  # Date when the service was added to the system
    service_details = models.CharField(max_length=100, null=True)  # Brief description of the service

    def __str__(self):
        """
        Returns a concise representation of the service, displaying the name and rate.
        """
        return f"{self.name} - ${self.rate_per_night} per night"

    def full_description(self):
        """
        Provides a detailed description of the service, including its name, details, and rate.

        Returns:
            str: Formatted string containing complete details of the service.
        """
        return (f"Service: {self.name}\n"
                f"Details: {self.service_details}\n"
                f"Rate per Night: ${self.rate_per_night}\n"
                f"Added on: {self.created_at.strftime('%Y-%m-%d %H:%M:%S')}")


from decimal import Decimal

# Reservation
class Reservation(models.Model):
    customer = models.ForeignKey('Customer', on_delete=models.CASCADE)  # Customer who made the reservation
    room = models.ForeignKey('Room', on_delete=models.SET_NULL, null=True)  # Room reserved by the customer
    date_in = models.DateField()  # Check-in date
    date_out = models.DateField()  # Check-out date
    total_cost = models.DecimalField(null=True,max_digits=8, decimal_places=2)  # Total cost for the stay
    is_active = models.BooleanField(default=True)  # Status of the reservation

    def __str__(self):
        """
        Returns a concise summary of the reservation, including customer and room information.
        """
        return f"Reservation for {self.customer.username} in Room {self.room.room_num if self.room else 'N/A'}"

    def calculate_total_nights(self):
        """
        Calculates the total room_num of nights for the reservation based on check-in and check-out dates.

        Returns:
            int: Number of nights the room is reserved for.
        """
        return (self.date_out - self.date_in).days

    def calculate_total_cost(self, additional_services_cost=Decimal(0)):
        """
        Calculates the total cost for the reservation, including room cost and any additional services.

        Args:
            additional_services_cost (Decimal): Optional additional cost for extra services.

        Returns:
            Decimal: Total cost including room rate and additional services.
        """
        if self.room and self.room.price_per_night is not None:
            room_cost = (self.room.price_per_night or Decimal(0)) * self.calculate_total_nights()
            self.total_cost = room_cost + additional_services_cost
            self.save()
            return self.total_cost
        return Decimal(0)

    def cancel_reservation(self):
        """
        Cancels the reservation by setting 'is_active' to False.

        Returns:
            str: Confirmation message of reservation cancellation.
        """
        self.is_active = False
        self.save()
        return f"Reservation for {self.customer.username} has been cancelled."



# ReservationService (Intermediate model for Many-to-Many relationship between Reservation and Services)
class ReservationService(models.Model):
    reservation = models.ForeignKey(Reservation, related_name='reservation_services', on_delete=models.CASCADE, null=True)
    extra_service = models.ForeignKey(Services, on_delete=models.CASCADE, null=True)
    count = models.PositiveIntegerField(default=1)  # Quantity of the service booked
    date_joined = models.DateTimeField(default=timezone.now)  # When the service was added to the reservation
    last_updated = models.DateTimeField(auto_now=True)  # When the reservation service details were last updated



# PaymentDetail (Dummy model for educational purposes only)
class PaymentDetail(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    name_on_card = models.CharField(max_length=120)
    card_type = models.CharField(max_length=60)
    card_number = models.CharField(max_length=18)  # Stored as a string for flexibility
    exp_month = models.PositiveSmallIntegerField(null=True, blank=True)
    exp_year = models.PositiveSmallIntegerField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)



# PaymentTransaction
class PaymentTransaction(models.Model):
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE)
    # Payment information used
    payment_detail = models.ForeignKey(PaymentDetail, on_delete=models.SET_NULL, null=True)
    # Amount paid in the transaction
    transaction_amount = models.DecimalField(max_digits=9, decimal_places=2)
    # Date when the transaction was processed
    transaction_date = models.DateTimeField(auto_now_add=True)
    # Payment method, e.g., 'Credit Card', 'Debit Card'
    transaction_method = models.CharField(max_length=50)
    # Status, e.g., 'Completed', 'Pending', 'Failed'
    transaction_status = models.CharField(max_length=50)
    # When the transaction record was created
    created_at = models.DateTimeField(default=timezone.now)
    # When the transaction record was last updated
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """
        Returns a string representation of the transaction, including the transaction amount,
        method, and status for easy identification.
        """
        return f"Transaction {self.id} - ${self.transaction_amount} via {self.transaction_method} ({self.transaction_status})"

    def get_payment_summary(self):
        """
        Generates a summary of the payment for logging or display purposes.
        Returns:
            str: Summary of the transaction details.
        """
        return (f"Transaction ID: {self.id}\n"
                f"Reservation ID: {self.reservation.id}\n"
                f"Amount: ${self.transaction_amount}\n"
                f"Method: {self.transaction_method}\n"
                f"Status: {self.transaction_status}\n"
                f"Date: {self.transaction_date.strftime('%Y-%m-%d %H:%M:%S')}")

