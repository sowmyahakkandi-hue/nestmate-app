from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator


class StudentProfile(models.Model):
    COURSE_CHOICES = [
        ('undergraduate', 'Undergraduate'),
        ('postgraduate', 'Postgraduate'),
        ('phd', 'PhD'),
        ('exchange', 'Exchange Student'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in format: '+999999999'. Up to 15 digits."
    )
    phone = models.CharField(validators=[phone_regex], max_length=17, blank=True)
    course = models.CharField(max_length=20, choices=COURSE_CHOICES, default='undergraduate')
    college = models.CharField(max_length=100)
    bio = models.TextField(max_length=500, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.college}"


class Listing(models.Model):
    PROPERTY_TYPES = [
        ('room', 'Single Room'),
        ('shared', 'Shared Room'),
        ('studio', 'Studio Apartment'),
        ('apartment', 'Full Apartment'),
    ]

    STATUS_CHOICES = [
        ('available', 'Available'),
        ('pending', 'Pending'),
        ('taken', 'Taken'),
    ]

    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='listings')
    title = models.CharField(max_length=200)
    description = models.TextField(max_length=1000)
    property_type = models.CharField(max_length=20, choices=PROPERTY_TYPES, default='room')
    address = models.CharField(max_length=300)
    city = models.CharField(max_length=100)
    rent_per_month = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(0.01)]
    )
    available_from = models.DateField()
    bedrooms = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(20)])
    bathrooms = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])
    max_occupants = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(20)])
    pets_allowed = models.BooleanField(default=False)
    smoking_allowed = models.BooleanField(default=False)
    wifi_included = models.BooleanField(default=False)
    bills_included = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} - €{self.rent_per_month}/month"


class RoommateRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('withdrawn', 'Withdrawn'),
    ]

    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='requests')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_requests')
    message = models.TextField(max_length=500)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        unique_together = ['listing', 'sender']

    def __str__(self):
        return f"Request from {self.sender.username} for {self.listing.title}"
