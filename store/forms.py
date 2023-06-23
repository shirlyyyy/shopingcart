from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField, PasswordChangeForm
from django.contrib.auth.models import User


class LoginForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs={'autofocus': 'True', 'class': 'form-control'}))
    password = forms.CharField(
        label='Password', widget=forms.PasswordInput(attrs={'autocomplete': 'current-password', 'class': 'form-control'})
    )


class CustomerRegistrationForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'autofocus': 'True', 'class': 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'autofocus': 'True', 'class': 'form-control'}))
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class MyPasswordResetForm(PasswordChangeForm):
    pass


class CheckoutForm(forms.Form):
    fname = forms.CharField(label='First Name')
    lname = forms.CharField(label='Last Name')
    address = forms.CharField(label='House Name')
    town = forms.CharField(label='City/Town')
    state = forms.CharField(label='State')
    card_number = forms.CharField(label='Card Number')
    card_expiry = forms.CharField(label='Card Expiry (MM/YY)')
    cvv = forms.CharField(label='CVV')
