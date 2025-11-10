from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Guesthouse(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    location_text = models.CharField(max_length=255, blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    contact_info = models.CharField(max_length=200, blank=True)
    rating = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.name

class RoomType(models.Model):
    guesthouse = models.ForeignKey(Guesthouse, related_name='rooms', on_delete=models.CASCADE)
    name = models.CharField(max_length=120)
    capacity = models.PositiveIntegerField(default=1)
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.guesthouse.name} — {self.name}"

class Package(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    base_price = models.DecimalField(max_digits=10, decimal_places=2)
    inclusions = models.JSONField(default=list, blank=True)  # list of inclusions

    def __str__(self):
        return self.title

class Transfer(models.Model):
    TRANSFER_TYPES = (
        ('speedboat', 'Speedboat'),
        ('seaplane', 'Seaplane'),
        ('other', 'Other'),
    )
    type = models.CharField(max_length=20, choices=TRANSFER_TYPES, default='speedboat')
    route = models.CharField(max_length=200)
    schedule = models.TextField(blank=True)  # free-form schedule
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.type} — {self.route}"

class Excursion(models.Model):
    title = models.CharField(max_length=200)
    duration = models.CharField(max_length=100, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    max_people = models.PositiveIntegerField(default=10)

    def __str__(self):
        return self.title

class Booking(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
    )
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    guest_name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=50, blank=True)
    guesthouse = models.ForeignKey(Guesthouse, null=True, blank=True, on_delete=models.SET_NULL)
    room_type = models.ForeignKey(RoomType, null=True, blank=True, on_delete=models.SET_NULL)
    check_in = models.DateField(null=True, blank=True)
    check_out = models.DateField(null=True, blank=True)
    booking_items = models.JSONField(default=dict, blank=True)  # extras, transfers, excursions etc
    total_price = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Booking {self.id} — {self.guest_name}"
