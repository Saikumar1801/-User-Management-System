# accounts/forms.py

from django import forms
from .models import Profile

class SignUpForm(forms.Form):
    USER_TYPE_CHOICES = (
        ("patient", "I am a Patient"),
        ("doctor", "I am a Doctor"),
    )
    
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    username = forms.CharField(max_length=150, required=True)
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)
    confirm_password = forms.CharField(widget=forms.PasswordInput, required=True)
    
    user_type = forms.ChoiceField(choices=USER_TYPE_CHOICES, widget=forms.RadioSelect, required=True)
    profile_picture = forms.ImageField(required=True)
    address_line1 = forms.CharField(max_length=255, required=True)
    city = forms.CharField(max_length=100, required=True)
    state = forms.CharField(max_length=100, required=True)
    pincode = forms.CharField(max_length=10, required=True)

    # This function is automatically called by Django to validate the form
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            # This will raise a validation error that is displayed to the user
            raise forms.ValidationError("Passwords do not match!")

        return cleaned_data