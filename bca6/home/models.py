from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
import uuid
from django.core.validators import MinValueValidator
from datetime import date
# Custom User Manager

# Custom User Manager
class UserProfileManager(BaseUserManager):
    def create_user(self, name, email, password=None, **extra_fields):
        if not name:
            raise ValueError("The Name field is required")
        if not email:
            raise ValueError("The Email field is required")

        email = self.normalize_email(email)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_admin", False)  # Default: non-admin

        user = self.model(name=name, email=email, **extra_fields)
        user.set_password(password)  # Hash password
        user.save(using=self._db)
        return user

    def create_superuser(self, name, email, password=None, **extra_fields):
        """Creates and returns a superuser with all privileges."""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_admin", True)  # ✅ Ensures Admin Privileges

        return self.create_user(name, email, password, **extra_fields)

# Custom User Model
class UserProfile(AbstractUser):
    username = None  # Remove username field
    name = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    gender = models.CharField(
        max_length=10,
        choices=[("Male", "Male"), ("Female", "Female"), ("Other", "Other")],
        blank=True,
        null=True,
    )

    is_staff = models.BooleanField(default=False)  # Required for Django Admin
    is_superuser = models.BooleanField(default=False)  # Required for Django Admin
    is_admin = models.BooleanField(default=False)  # Custom admin flag

    USERNAME_FIELD = "email"  # ✅ Use email for authentication
    REQUIRED_FIELDS = ["name"]

    objects = UserProfileManager()  # Use custom manager

    def __str__(self):
        return self.name

    def has_perm(self, perm, obj=None):
        return self.is_superuser  # ✅ Superusers get all permissions

    def has_module_perms(self, app_label):
        return self.is_superuser  # ✅ Superusers access all apps
    

class TableBooking(models.Model):
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=15)
    email = models.EmailField(null=True)
    num_people = models.IntegerField()
    num_tables = models.IntegerField()
    booking_time = models.DateTimeField()
    status = models.CharField(
        max_length=20, 
        choices=[('Available', 'Available'), ('Booked', 'Booked')], 
        default='Available'
    )

    def __str__(self):
        return f"{self.name} - {self.booking_time.strftime('%Y-%m-%d %H:%M')}"

class BookingSlot(models.Model):
    slot_time = models.CharField(max_length=20, unique=True,null=True)  # Stores time as a string (e.g., "11:00 AM - 11:30 AM")
    available_tables = models.IntegerField(default=20)  # Adjust based on restaurant capacity

    def __str__(self):
        return self.slot_time

    @staticmethod
    def get_predefined_slots():
        """Returns predefined lunch and dinner time slots."""
        return [
            "11:00 AM - 11:30 AM", "11:30 AM - 12:00 PM", "12:00 PM - 12:30 PM", "12:30 PM - 1:00 PM",
            "1:00 PM - 1:30 PM", "1:30 PM - 2:00 PM", "2:00 PM - 2:30 PM", "2:30 PM - 3:00 PM",
            "6:30 PM - 7:00 PM", "7:00 PM - 7:30 PM", "7:30 PM - 8:00 PM", "8:00 PM - 8:30 PM",
            "8:30 PM - 9:00 PM", "9:00 PM - 9:30 PM", "9:30 PM - 10:00 PM", "10:00 PM - 10:30 PM",
            "10:30 PM - 11:00 PM"
        ]

class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    image = models.ImageField(upload_to='category_images/', blank=True, null=True)  # Added image field
    

    def __str__(self):
        return self.name

class Subcategory(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="subcategories")
    image = models.ImageField(upload_to='subcategory_images/', blank=True, null=True)  # Added image field
    

    def __str__(self):
        return self.name
    
class Menu(models.Model):
    name = models.CharField(max_length=255)
    subcategory = models.ForeignKey("Subcategory", on_delete=models.CASCADE, related_name="foods")
    price = models.DecimalField(max_digits=10, decimal_places=2,validators=[MinValueValidator(0.01)])  # Prevent negative or zero prices)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to="food_images/", blank=True, null=True)  # ImageField for file upload
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        """ Ensure price is always positive before saving """
        if self.price < 0:
            self.price = abs(self.price)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

#cart
class Cart(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    food = models.ForeignKey('Menu', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.food.name} - {self.user.email}"
    

class Event(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(default="No description entered")
    image = models.ImageField(upload_to='events/', null=True, blank=True)  # Allows blank images
    location = models.CharField(max_length=255, default="Not specified")

    def __str__(self):  # Fixing str method
        return self.name

class EventDetails(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="details")  # 1:N Relationship
    name = models.CharField(max_length=200, null=True)
    long_description = models.TextField()
    additional_images = models.ImageField(upload_to='event_details/', null=True, blank=True)
    charge = models.DecimalField(max_digits=10, decimal_places=2, null=True)

    def __str__(self):  # Fixing str method
        return f"Details for {self.event.name}"

from django.core.exceptions import ValidationError
from django.utils.timezone import now
class EventBooking(models.Model):
    event = models.ForeignKey("Event", on_delete=models.CASCADE, related_name="bookings")  
    name = models.CharField(max_length=255)
    email = models.EmailField()
    date = models.DateField()
    time = models.TimeField()
    no_of_persons = models.IntegerField()
    advance_charges = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def clean(self):
        # Restrict Past Dates
        if self.date < now().date():
            raise ValidationError("You cannot select a past date.")

        # Restrict Booking for Fully Booked Dates
        if EventBooking.objects.filter(date=self.date).exists():
            raise ValidationError("This date is already fully booked.")

        # Restrict Past Times for Today's Date
        if self.date == now().date() and self.time < now().time():
            raise ValidationError("You cannot select a past time.")

    def save(self, *args, **kwargs):
        self.clean()  # Run the validations before saving
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Booking for {self.event.name} by {self.name}"

class Order(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    table_no = models.PositiveIntegerField(default=1, blank=True, null=True)

    def __str__(self):
        return f"Order {self.id} by {self.user.email}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    food = models.ForeignKey(Menu, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Store price at checkout time

    def __str__(self):
        return f"{self.quantity} x {self.food.name} - Order {self.order.id}"

class Manage_Table(models.Model):
    table_number = models.IntegerField(unique=True)
    capacity = models.IntegerField()
    is_occupied = models.BooleanField(default=False)

    def __str__(self):
        return f"Table {self.table_number} (Capacity: {self.capacity})"

class DiscountOffer(models.Model):
    offer_id = models.AutoField(primary_key=True)
    offer_start_date = models.DateField()
    offer_end_date = models.DateField()
    offer_desc = models.CharField(max_length=35)
    discount_percentage = models.IntegerField()
    # category = models.ForeignKey(Category, on_delete=models.CASCADE,null=True)

    def str(self):
        return self.offer_desc
    
    @classmethod
    def delete_expired_offers(cls):
        today = date.today()
        cls.objects.filter(offer_end_date__lt=today).delete()



class Feedback(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    feedback = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Complaint from {self.name} ({self.email})"

