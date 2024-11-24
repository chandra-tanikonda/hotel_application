# forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import Customer
from .models import Reservation

User = get_user_model()

class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['first_name', 'last_name', 'email', 'mobile_number', 'address1', 'apt_number', 'city', 'state', 'zip_code']

from django.contrib.auth.forms import AuthenticationForm
class CustomerSignupForm(forms.ModelForm):
    username = forms.CharField(max_length=10, label="Mobile Number")
    first_name = forms.CharField(max_length=60, required=True)
    last_name = forms.CharField(max_length=60, required=True)
    email = forms.EmailField(max_length=60, required=True)
    password = forms.CharField(widget=forms.PasswordInput, label="Password")
    address = forms.CharField(max_length=200,required=True)
    class Meta:
        model = Customer
        fields = ('username', 'first_name', 'last_name', 'email','address' ,'password')

    def __init__(self, *args, **kwargs):
        super(CustomerSignupForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        user = super(CustomerSignupForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

class UserLoginForm(AuthenticationForm):
    username = forms.CharField(max_length=10, label="Mobile Number", widget=forms.TextInput(attrs={'placeholder': 'Mobile Number'}))
    password = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))

    def __init__(self, request=None, *args, **kwargs):
        super(UserLoginForm, self).__init__(request, *args, **kwargs)

class BookingForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['date_in', 'date_out']
        widgets = {
            'date_in': forms.DateInput(attrs={'type': 'date'}),
            'date_out': forms.DateInput(attrs={'type': 'date'}),
        }

from .models import ReservationService, Services

class ServiceForm(forms.Form):
    services = forms.ModelMultipleChoiceField(
        queryset=Services.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

from .models import PaymentDetail

class CreditCardForm(forms.ModelForm):
    class Meta:
        model = PaymentDetail
        fields = ['card_number', 'exp_month', 'exp_year']
        widgets = {
            'exp_month': forms.NumberInput(attrs={'placeholder': 'MM', 'class': 'form-control'}),
            'exp_year': forms.NumberInput(attrs={'placeholder': 'YYYY', 'class': 'form-control'})
            ,
        }

# forms.py

from django import forms
from .models import Room

class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['room_num', 'room_type', 'room_capacity', 'price_per_night', 'is_available', 'image', 'details']


from .models import Services

class AddServiceForm(forms.ModelForm):
    class Meta:
        model = Services
        fields = ['name','service_details']

