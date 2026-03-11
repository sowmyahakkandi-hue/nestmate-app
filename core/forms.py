from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import StudentProfile, Listing, RoommateRequest
import re


class RegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=50, required=True)
    last_name = forms.CharField(max_length=50, required=True)
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("A user with this email already exists.")
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not re.match(r'^[a-zA-Z0-9_]+$', username):
            raise forms.ValidationError("Username can only contain letters, numbers, and underscores.")
        return username


class StudentProfileForm(forms.ModelForm):
    class Meta:
        model = StudentProfile
        fields = ['phone', 'course', 'college', 'bio']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4}),
        }

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if phone and not re.match(r'^\+?1?\d{9,15}$', phone):
            raise forms.ValidationError("Enter a valid phone number.")
        return phone

    def clean_college(self):
        college = self.cleaned_data.get('college')
        if college and len(college) < 3:
            raise forms.ValidationError("College name must be at least 3 characters.")
        return college


class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = [
            'title', 'description', 'property_type', 'address', 'city',
            'rent_per_month', 'available_from', 'bedrooms', 'bathrooms',
            'max_occupants', 'pets_allowed', 'smoking_allowed',
            'wifi_included', 'bills_included', 'status'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'available_from': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean_rent_per_month(self):
        rent = self.cleaned_data.get('rent_per_month')
        if rent and rent <= 0:
            raise forms.ValidationError("Rent must be a positive number.")
        if rent and rent > 99999:
            raise forms.ValidationError("Rent value seems too high. Please check.")
        return rent

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if title and len(title) < 5:
            raise forms.ValidationError("Title must be at least 5 characters.")
        return title

    def clean(self):
        cleaned_data = super().clean()
        bedrooms = cleaned_data.get('bedrooms')
        max_occupants = cleaned_data.get('max_occupants')
        if bedrooms and max_occupants and max_occupants < bedrooms:
            raise forms.ValidationError("Max occupants cannot be less than number of bedrooms.")
        return cleaned_data


class RoommateRequestForm(forms.ModelForm):
    class Meta:
        model = RoommateRequest
        fields = ['message']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Introduce yourself and explain why you\'re interested...'}),
        }

    def clean_message(self):
        message = self.cleaned_data.get('message')
        if message and len(message) < 20:
            raise forms.ValidationError("Message must be at least 20 characters.")
        return message
