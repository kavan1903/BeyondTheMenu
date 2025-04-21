from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth import authenticate,login as auth_login
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from home.models import *
from django.contrib.auth import authenticate, login
import re
import json
from django.http import JsonResponse#for update cart
from django.views.decorators.csrf import csrf_exempt #For add_to_cart
from django.contrib.admin.views.decorators import staff_member_required
import razorpay

# Create your views here.
def home(request):
    return render(request,"index.html")

def about(request):
    return render(request,"about.html")

def event(request):
    return render(request,"event.html")

# def menu(request):
#     return render(request,"menu.html")

# def booking(request):
#     return render(request,"booking.html")

def team(request):
    return render(request,"team.html")

def testimonial(request):
    return render(request,"testimonial.html")

from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.contrib import messages

def Contact(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        message = request.POST.get("message")

        if not all([name, email, phone, message]):  # Ensure all fields are filled
            messages.error(request, "All fields are required!")
            return redirect("contact")

        from_email = "malharexoticaa@gmail.com"  # Admin email (also used as sender)
        admin_email = "malharexoticaa@gmail.com"  # Admin receives the inquiry

        # Notify admin about the new contact inquiry
        admin_subject = "New Contact Inquiry"
        admin_message = f"New contact inquiry received:\n\nName: {name}\nEmail: {email}\nPhone: {phone}\n\nMessage:\n{message}"

        try:
            send_mail(admin_subject, admin_message, from_email, [admin_email])
        except Exception as e:
            messages.error(request, "Failed to send email to admin.")
            print(f"Admin Email Error: {e}")  # Debugging purpose

        # Send confirmation email to user
        user_subject = "Contact Form Submission Confirmation"
        user_message = f"Hello {name},\n\nThank you for reaching out! We have received your message and will get back to you soon.\n\nYour Message:\n{message}\n\nBest regards,\nRestaurant Team"

        try:
            send_mail(user_subject, user_message, from_email, [email])
        except Exception as e:
            messages.error(request, "Failed to send confirmation email.")
            print(f"User Email Error: {e}")  # Debugging purpose

        messages.success(request, "Your message has been sent successfully! A confirmation email has been sent to you.")
        return redirect("contact")

    return render(request, "contact.html")


def signup(request):
    if request.method == "POST":
        errors = []
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        gender = request.POST.get('gender')
        password = request.POST.get('password')
        confpass = request.POST.get('confpass')

        # Validate email format and uniqueness
        if not email:
            errors.append("Email is required")
        else:
            try:
                validate_email(email)
                if UserProfile.objects.filter(email=email).exists():
                    errors.append("Email already registered")
            except ValidationError:
                errors.append("Invalid email format")

        # Validate phone number (Only 10 digits allowed)
        if not phone:
            errors.append("Phone number is required")
        elif not re.fullmatch(r'\d{10}', phone):  # Ensures exactly 10 digits
            errors.append("Phone number must be exactly 10 digits")

        # Validate password
        if not password:
            errors.append("Password is required")
        elif len(password) < 8 or len(password) > 12:
            errors.append("Password length must be between 8 to 12 characters")
        elif not any(char in "@_&" for char in password):
            errors.append("Password must include at least one special symbol (@, _, &)")

        # Confirm password validation
        if not confpass:
            errors.append("Confirm password is required")
        elif password != confpass:
            errors.append("Passwords do not match")

        # If there are errors, return them to the signup page
        if errors:
            return render(request, "signup.html", {"errors": errors})

        try:
            # Save user in UserProfile model
            my_user = UserProfile.objects.create(
                name=name,
                email=email,
                phone=phone,
                gender=gender,
                password=password  
            )

            messages.success(request, "Account created successfully! Please log in.")
            return redirect('signin')
        except Exception as e:
            messages.error(request, f"Error: {e}")

    return render(request, "signup.html")


def signin(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = UserProfile.objects.get(email=email, password=password)  # Authenticate manually
            login(request, user)  # Log in the user
            request.session['user_id'] = user.id
            request.session['user_name'] = user.name
            request.session['user_email'] = user.email
            request.session['user_gender'] = user.gender
            request.session['user_phone'] = user.phone
            return redirect("home")
        except UserProfile.DoesNotExist:
            messages.error(request, "Incorrect email or password!")

    return render(request, "login.html")

from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.contrib import messages
from home.models import UserProfile  

def admin_signin(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            user = UserProfile.objects.get(email=email)

            if not user.check_password(password):  # Use Django's password verification
                messages.error(request, "Incorrect email or password!")
                return render(request, "admin_login.html")

            if user.is_admin:  
                login(request, user)  
                return redirect("admin_dashboard")  
            else:
                messages.error(request, "Access Denied! You are not an admin.")

        except UserProfile.DoesNotExist:
            messages.error(request, "Incorrect email or password!")

    return render(request, "admin_login.html")





def logout(request):
    # logout(request)
    request.session.flush()  # Clears session
    return redirect('signin')

#Profile
from django.contrib.auth import get_user_model
User = get_user_model()

@login_required(login_url='signin')
def prof(request):
    if 'user_id' not in request.session:
        return redirect("signin")
    
    user = User.objects.get(id=request.session['user_id'])
    
    context = {
        'username': user.name,
        'email': user.email,
        'gender': user.gender,
        'phone_number': user.phone,
    }
    return render(request, 'profile.html', context)

# Edit Profile View (Form for Editing)
@login_required(login_url='signin')
def edit_prof(request):
    if 'user_id' not in request.session:
        return redirect("signin")
    
    user = User.objects.get(id=request.session['user_id'])

    if request.method == "POST":
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        gender = request.POST.get('gender')

        user.email = email
        user.phone = phone_number  # Assuming phone_number exists in your custom user model
        user.gender = gender  # Assuming gender exists in your custom user model
        user.save()

        # Update session data
        request.session['user_email'] = email
        request.session['user_phone'] = phone_number
        request.session['user_gender'] = gender

        messages.success(request, "Profile updated successfully!")
        return redirect('prof')  # Redirect to profile page after successful update

    context = {
        'username': user.name,
        'email': user.email,
        'gender': user.gender,
        'phone_number': user.phone,
    }
    return render(request, 'EditProfile.html',context)


def errorpage(request):
    return render(request,"error.html")


import razorpay
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from datetime import datetime, timedelta
from .models import TableBooking, BookingSlot

razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

def assign_tables(num_people):
    """Assigns the correct number of tables based on the number of people."""
    if num_people <= 4:
        return 1
    elif num_people <= 6:
        return 2
    elif num_people <= 10:
        return 3
    return 0  # Invalid input

def get_all_slots():
    """Fetches all booking slots and marks availability."""
    slots = BookingSlot.objects.all()
    all_slots = []

    for slot in slots:
        booked_tables = TableBooking.objects.filter(
            booking_time__time=slot.slot_time
        ).count()

        available_tables = slot.available_tables - booked_tables
        is_available = available_tables > 0  # Check if tables are available

        all_slots.append({
            "slot_time": slot.slot_time,  # No need for strftime
            "available_tables": available_tables,
            "is_available": is_available
        })

    return all_slots

def book_table(request):
    slots = get_all_slots()  # Fetch all slots
    context = {
        "slots": slots,
        "people_range": range(1, 11),  # Pass range from 1 to 10
    }

    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        phone = request.POST.get("phone", "").strip()
        email = request.POST.get("email", "").strip()
        num_people = request.POST.get("people", "").strip()
        slot_time = request.POST.get("slot_time", "").strip()

        if not name or not phone or not email or not num_people or not slot_time:
            context["error"] = "All fields are required!"
            return render(request, "booking.html", context)

        try:
            num_people = int(num_people)
        except ValueError:
            context["error"] = "Invalid number of people!"
            return render(request, "booking.html", context)

        num_tables_needed = assign_tables(num_people)

        # Check if the selected slot is available
        selected_slot = next((slot for slot in slots if slot["slot_time"] == slot_time), None)

        if not selected_slot or not selected_slot["is_available"]:
            context["error"] = "Selected time slot is not available!"
            return render(request, "booking.html", context)

        # Razorpay expects the amount in paise (INR * 100)
        amount = 600000 if num_people <= 5 else 1000000  

        try:
            # Create Razorpay order
            payment_order = razorpay_client.order.create({
                "amount": amount,  # Amount in paise
                "currency": "INR",
                "payment_capture": 1,  
            })
        except razorpay.errors.RazorpayError:
            context["error"] = "Payment processing error. Please try again later."
            return render(request, "booking.html", context)

        # Store booking details in session
        request.session["booking_data"] = {
            "name": name,
            "phone": phone,
            "email": email,
            "num_people": num_people,
            "num_tables": num_tables_needed,
            "slot_time": slot_time,
            "razorpay_order_id": payment_order["id"],
        }

        return render(request, "payment.html", {
            "razorpay_order_id": payment_order["id"],
            "razorpay_key": settings.RAZORPAY_KEY_ID,
            "amount": amount // 100,  # Convert back to rupees
            "currency": "INR",
        })

    return render(request, "booking.html", context)

@csrf_exempt
def payment_success(request):
    booking_data = {
        "name": request.POST.get("name"),
        "phone": request.POST.get("phone"),
        "email": request.POST.get("email"),
        "num_people": request.POST.get("people"),
        "booking_date": request.POST.get("booking_date"),
        "num_tables":1 ,
        "slot_time": request.POST.get("time_slot"),
    }

    if not booking_data:
        return redirect("home")


    # Convert slot_time to a full datetime object
    slot_time_str = booking_data["slot_time"].split("-")[0]  # Extract start time (e.g., "11:00 AM")
    date_str = f"{booking_data['booking_date']} {slot_time_str}".strip()
    booking_datetime = datetime.strptime(date_str, "%Y-%m-%d %H:%M")
    

    # Send email confirmation
    subject = "Table Booking Confirmation - Beyond the Menu"
    message = (
        f"Hello {booking_data['name']},\n\n"
        f"Your table booking is confirmed!\n"
        f"Number of People: {booking_data['num_people']}\n"
        f"Tables Reserved: {booking_data['num_tables']}\n"
        f"Time Slot: {booking_data['slot_time']}\n"
        "Thank you for choosing Beyond the Menu!\n\n"
        "Best Regards,\n"
        "Beyond the Menu Team"
    )
    recipient_email = booking_data["email"]
    
    try:
        send_mail(subject, message, settings.EMAIL_HOST_USER, [recipient_email])
        print("mail sent")
    except Exception as e:
        print(f"Email sending error: {e}")

    # Save booking in database
    TableBooking.objects.create(
        name=booking_data["name"],
        phone=booking_data["phone"],
        email=booking_data["email"],
        num_people=booking_data["num_people"],
        num_tables=booking_data["num_tables"],
        booking_time=booking_datetime,  # Now it's a full datetime object
        status="Booked"
    )
    
    return render(request, "success.html", {
    "booking_success": True,
})


#menu design
def category(request):
    categories = Category.objects.all()
    return render(request, 'category.html', {'categories': categories})

# Subcategory View
def sub_category(request, category_name):
    category = get_object_or_404(Category, name=category_name)
    subcategories = Subcategory.objects.filter(category=category)
    return render(request, 'subcategory.html', {'category': category, 'subcategories': subcategories})

# Food Menu View
def food_menu(request, subcategory_name):
    subcategory = get_object_or_404(Subcategory, name=subcategory_name)
    foods = Menu.objects.filter(subcategory=subcategory)
    return render(request, 'foodmenu.html', {'subcategory': subcategory, 'foods': foods})

# View Cart

def menu_view(request):
    categories = Category.objects.prefetch_related('subcategories').all()
    category_id = request.GET.get("category")
    subcategory_id = request.GET.get("subcategory")

    selected_subcategory = int(subcategory_id) if subcategory_id else None
    selected_category = category_id

    if selected_subcategory:
        menu_items = Menu.objects.filter(subcategory_id=selected_subcategory)
    elif category_id:
        menu_items = Menu.objects.filter(subcategory__category_id=category_id)
    else:
        menu_items = Menu.objects.all()

    cart_items = Cart.objects.filter(user=request.user) if request.user.is_authenticated else []
    cart_dict = {str(item.food.id): item.quantity for item in cart_items}

    return render(request, "menu.html", {
        "categories": categories,
        "menu_items": menu_items,
        "cart_dict": cart_dict,
        "selected_category": selected_category,
        "selected_subcategory": selected_subcategory,
    })

@login_required
def add_to_cart(request, food_id):
    food = get_object_or_404(Menu, id=food_id)
    cart_item, created = Cart.objects.get_or_create(user=request.user, food=food)

    if not created:
        cart_item.quantity += 1  # Increase quantity if item already in the cart
    
    cart_item.save()

    # Return updated cart details
    cart_items = Cart.objects.filter(user=request.user)
    cart_dict = {str(item.food.id): item.quantity for item in cart_items}

    return JsonResponse({
        'quantity': cart_item.quantity,
        'cart_dict': cart_dict
    })


@login_required
def update_cart(request, food_id, action):
    # Get the cart item for the specified food_id
    cart_item = get_object_or_404(Cart, user=request.user, food_id=food_id)

    # Handle action (increase or decrease the quantity)
    if action == 'increase':
        cart_item.quantity += 1
    elif action == 'decrease':
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
        else:
            cart_item.delete()  # Remove the item if quantity is 0
            return JsonResponse({
                'quantity': 0,
                'removed': True,
                'new_total_price': get_cart_total_price(request.user)  # Send updated total price after item removal
            })

    cart_item.save()  # Save the cart item after updating the quantity

    # Return the updated quantity and the total price of the cart
    return JsonResponse({
        'quantity': cart_item.quantity,
        'new_total_price': get_cart_total_price(request.user)  # Always include the total price
    })

# Function to calculate the total price of all cart items for the user
def get_cart_total_price(user):
    cart_items = Cart.objects.filter(user=user)
    return sum(item.food.price * item.quantity for item in cart_items)


@login_required
def cart_view(request):
    cart_items = Cart.objects.filter(user=request.user)
    cart = {}
    total_price = 0
    # cart_count = sum(item.quantity for item in cart_items)  # Count total items

    for item in cart_items:
        category_name = item.food.subcategory.category.name
        subcategory_name = item.food.subcategory.name

        if category_name not in cart:
            cart[category_name] = []

        cart[category_name].append({
            "id": item.food.id,
            "name": item.food.name,
            "image": item.food.image.url if item.food.image else "",
            "price": item.food.price,
            "quantity": item.quantity,
            "subcategory": subcategory_name,
        })
        total_price += item.food.price * item.quantity

    return render(request, "addtocart.html", {"cart": cart, "total_price":total_price})

import razorpay
from django.utils.timezone import now
razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

@login_required
def checkout(request):
    user_profile = request.user  
    cart_items = Cart.objects.filter(user=user_profile)

    if not cart_items.exists():
        return HttpResponse("Your cart is empty", status=400)

    # Calculate total for each cart item
    for item in cart_items:
        item.total_price = item.quantity * item.food.price  # Compute total price for each item

    # Calculate total bill amount
    total_amount = sum(item.total_price for item in cart_items)

    # Get the highest available discount offer
    active_offers = DiscountOffer.objects.filter(
        offer_start_date__lte=now(), offer_end_date__gte=now()
    ).order_by('-discount_percentage')
    
    discount_percentage = active_offers.first().discount_percentage if active_offers.exists() else 0

    # Calculate total discount
    discounted_amount = (total_amount * discount_percentage) / 100

    # Final amount after discount
    final_amount = total_amount - discounted_amount

    context = {
        "name": getattr(user_profile, "name", "Guest"),
        "email": getattr(user_profile, "email", ""),
        "phone": getattr(user_profile, "phone", ""),
        "cart_items": cart_items,
        "total_amount": round(total_amount, 2),
        "discount_percentage": discount_percentage,
        "discounted_amount": round(discounted_amount, 2),
        "final_amount": round(final_amount, 2),
        "razorpay_key": settings.RAZORPAY_KEY_ID,
        "offers": active_offers,
    }

    return render(request, 'checkout.html', context)


def filter_menu(request):
    category_id = request.GET.get("category")
    subcategory_id = request.GET.get("subcategory")

    filtered_items = Menu.objects.all()

    if category_id:
        filtered_items = filtered_items.filter(subcategory__category__id=category_id)

    if subcategory_id:
        filtered_items = filtered_items.filter(subcategory__id=subcategory_id)

    return render(request, "menu_items.html", {"menu_items": filtered_items})


@staff_member_required  # Ensures only admin users can access
def admin_dashboard(request):
    return render(request, "admin/custom_dashboard.html")  # Ensure the template is in templates/


#Event
def event_list(request):
    """View to list all events"""
    events = Event.objects.all().prefetch_related("details")  # Optimized query
    return render(request, 'event.html', {'events': events})

def event_details(request, event_id):
    """View to display event details"""
    event = get_object_or_404(Event, id=event_id)
    event_details = EventDetails.objects.filter(event=event)  # Get all matching details
    return render(request, 'event_detail.html', {'event': event, 'event_details': event_details})

# from django.utils.timezone import now, make_aware
# from datetime import datetime

# @login_required(login_url="/signin/")
# def event_booking(request, event_id, detail_id):
#     event = get_object_or_404(Event, id=event_id)
#     event_detail = get_object_or_404(EventDetails, id=detail_id, event=event)

#     # Calculate advance charge as 1/4 of total charge
#     advance_charge = event_detail.charge / 4  

#     if request.method == "POST":
#         name = request.POST.get("name").strip()
#         email = request.POST.get("email").strip()
#         date = request.POST.get("date").strip()
#         time = request.POST.get("time").strip()
#         no_of_persons = request.POST.get("no_of_persons").strip()
#         charge = request.POST.get("charges").strip()  # Advance Charge

#         # Validation checks
#         if not name or not email or not date or not time or not no_of_persons:
#             messages.error(request, "All fields are required.")
#             return redirect("event_booking", event_id=event_id, detail_id=detail_id)

#         try:
#             event_datetime = make_aware(datetime.strptime(f"{date} {time}", "%Y-%m-%d %H:%M"))
#         except ValueError:
#             messages.error(request, "Invalid date or time format.")
#             return redirect("event_booking", event_id=event_id, detail_id=detail_id)

#         if event_datetime < now():
#             messages.error(request, "Event date and time must be in the future.")
#             return redirect("event_booking", event_id=event_id, detail_id=detail_id)

#         if int(no_of_persons) < 1:
#             messages.error(request, "Number of persons must be at least 1.")
#             return redirect("event_booking", event_id=event_id, detail_id=detail_id)

#         # Save booking to the database
#         booking = EventBooking.objects.create(
#             event=event,
#             name=name,
#             email=email,
#             date=date,
#             time=time,
#             no_of_persons=no_of_persons,
#             advance_charges=charge,  # Save advance charge
#         )

#         # Send confirmation email
#         subject = "Event Booking Confirmation"
#         message = (
#             f"Hello {name},\n\n"
#             f"Your event booking has been confirmed!\n\n"
#             f"**Event Details:**\n"
#             f" Event: {event.name}\n"
#             f" Date: {date}\n"
#             f" Time: {time}\n"
#             f" No. of Persons: {no_of_persons}\n"
#             f" Advance Charge Paid: ₹{charge}\n\n"
#             f"Thank you for booking with us!\n\n"
#             f"Best Regards,\nBeyond The Menu"
#         )

#         from_email = "malharexoticaa@gmail.com"
#         recipient_list = [email]

#         send_mail(subject, message, from_email, recipient_list, fail_silently=False)

#         messages.success(request, "Event booked successfully! A confirmation email has been sent.")
#         return redirect("event_list")

#     return render(request, "event_booking.html", {"event_detail": event_detail, "event": event, "advance_charge": advance_charge})

import io
from django.http import FileResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.timezone import now, make_aware
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import EmailMessage
from django.conf import settings
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from .models import Event, EventDetails, EventBooking

from django.http import JsonResponse
from django.utils.timezone import now
from datetime import timedelta

@login_required(login_url="/signin/")
def event_booking(request, event_id, detail_id):
    event = get_object_or_404(Event, id=event_id)
    event_detail = get_object_or_404(EventDetails, id=detail_id, event=event)

    advance_charge = event_detail.charge / 4  # 1/4th of total charge

    if request.method == "POST":
        name = request.POST.get("name").strip()
        email = request.POST.get("email").strip()
        date = request.POST.get("date").strip()
        time = request.POST.get("time").strip()
        no_of_persons = request.POST.get("no_of_persons").strip()
        charge = request.POST.get("charges").strip()  # Advance Charge

        # Validate all fields
        if not name or not email or not date or not time or not no_of_persons:
            messages.error(request, "All fields are required.")
            return redirect("event_booking", event_id=event_id, detail_id=detail_id)

        try:
            event_date = datetime.strptime(date, "%Y-%m-%d").date()
        except ValueError:
            messages.error(request, "Invalid date format.")
            return redirect("event_booking", event_id=event_id, detail_id=detail_id)

        today = now().date()
        min_booking_date = today + timedelta(days=5)  # Users must book at least 5 days in advance
        max_booking_date = today + timedelta(days=90)  # Restriction of 3 months

        # *Validation: No Past Dates*
        if event_date < today:
            messages.error(request, "You cannot select a past date.")
            return redirect("event_booking", event_id=event_id, detail_id=detail_id)

        # *Validation: Must Book at Least 5 Days in Advance*
        if event_date < min_booking_date:
            messages.error(request, "Event booking must be done at least 5 days in advance.")
            return redirect("event_booking", event_id=event_id, detail_id=detail_id)

        # *Validation: Cannot Book More than 3 Months in Advance*
        if event_date > max_booking_date:
            messages.error(request, "You can only book within the next 3 months.")
            return redirect("event_booking", event_id=event_id, detail_id=detail_id)

        # *Validation: Restrict Full-Day Booking*
        if EventBooking.objects.filter(date=date).exists():
            messages.error(request, "This date is fully booked. Please choose another date.")
            return redirect("event_booking", event_id=event_id, detail_id=detail_id)

        # Save booking
        booking = EventBooking.objects.create(
            event=event,
            name=name,
            email=email,
            date=event_date,  # ✅ Pass the converted date
            time=time,
            no_of_persons=int(no_of_persons),  # ✅ Convert to integer
            advance_charges=float(charge),  # ✅ Convert to float for safety
        )

        # Generate PDF Receipt
        pdf_buffer = generate_pdf_receipt(name, event.name, date, time, no_of_persons, charge)

        # Send Confirmation Email with PDF Attachment
        send_booking_email(name, email, event.name, date, time, no_of_persons, charge, pdf_buffer)

        messages.success(request, "Event booked successfully! A confirmation email with the invoice has been sent.")
        return redirect("event_list")

    return render(request, "event_booking.html", {"event_detail": event_detail, "event": event, "advance_charge": advance_charge})


def check_double_booking(request):
    if request.method == "POST":
        event_date = request.POST.get("date")

        # Check if any event exists on that date
        exists = EventBooking.objects.filter(date=event_date).exists()

        return JsonResponse({"exists":exists})



    
import io
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

import io
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import simpleSplit

def generate_pdf_receipt(name, event_name, date, time, no_of_persons, charge):
    """Generates a professional PDF receipt with enhanced styling"""
    buffer = io.BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=letter)
    pdf.setTitle("Event Booking Receipt")

    # Header Section with Gold Color
    pdf.setFillColor(colors.gold)
    pdf.setFont("Helvetica-Bold", 18)
    pdf.drawString(170, 760, "Malhar Exotica - Event Receipt")

    # Separator Line
    pdf.setStrokeColor(colors.gold)
    pdf.setLineWidth(2)
    pdf.line(50, 745, 550, 745)

    # Content Styling
    pdf.setFont("Helvetica", 12)
    pdf.setFillColor(colors.black)

    # Adjust vertical positioning
    y_position = 700
    line_gap = 20

    # Event Details (Formatted Like a Table)
    details = [
        ("Customer Name:", name),
        ("Event Name:", event_name),
        ("Event Date:", date),
        ("Event Time:", time),
        ("Number of Persons:", no_of_persons),
        ("Amount Paid (Advance):", charge)
    ]

    for label, value in details:
        pdf.setFont("Helvetica-Bold", 12)
        pdf.drawString(50, y_position, label)  # Label in bold
        pdf.setFont("Helvetica", 12)
        pdf.drawString(200, y_position, str(value))  # Value aligned
        y_position -= line_gap  # Move to next line

    # Footer Styling in Dark Green
    pdf.setFont("Helvetica-Oblique", 10)
    pdf.setFillColor(colors.darkgreen)
    pdf.drawString(50, 550, "Thank you for booking with us!")
    pdf.drawString(50, 530, "For any queries, contact us at support@malharexotica.com")

    pdf.showPage()
    pdf.save()
    
    buffer.seek(0)
    return buffer  # ✅ FIX: Ensure the function returns the buffer

def send_booking_email(name, email, event_name, date, time, no_of_persons, charge, pdf_buffer):
    """ Sends an email with the booking details and the attached PDF receipt """
    subject = "Event Booking Confirmation & Receipt"
    message = (
        f"Hello {name},\n\n"
        f"Your event booking has been confirmed!\n\n"
        f"Event: {event_name}\n"
        f"Date: {date}\n"
        f"Time: {time}\n"
        f"Number of Persons: {no_of_persons}\n"
        f"Advance Amount Paid: ₹{charge}\n\n"
        f"Attached is your booking receipt.\n\n"
        f"Thank you for choosing Beyond The Menu!\n"
    )

    email_msg = EmailMessage(subject, message, settings.DEFAULT_FROM_EMAIL, [email])
    email_msg.attach("Event_Receipt.pdf", pdf_buffer.getvalue(), "application/pdf")
    email_msg.send()

# from django.http import JsonResponse
# from django.core.mail import EmailMessage
# from django.conf import settings
# from io import BytesIO

# def send_booking_email(request):
#     if request.method == "POST":
#         event_name = request.POST.get("event")
#         date = request.POST.get("date")
#         time = request.POST.get("time")
#         no_of_persons = request.POST.get("persons")
#         email = request.POST.get("email")
#         charge = request.POST.get("charge")

#         # Create a simple PDF buffer (optional, adjust as needed)
#         pdf_buffer = BytesIO()
#         pdf_buffer.write(f"Event: {event_name}\nDate: {date}\nTime: {time}\nPersons: {no_of_persons}\nCharge: ₹{charge}".encode())

#         # Send Email
#         subject = "Event Booking Confirmation & Receipt"
#         message = (
#             f"Hello,\n\nYour event booking has been confirmed!\n\n"
#             f"Event: {event_name}\nDate: {date}\nTime: {time}\nPersons: {no_of_persons}\nCharge Paid: ₹{charge}\n\n"
#             f"Thank you for choosing Beyond The Menu!\n"
#         )
#         email_msg = EmailMessage(subject, message, settings.DEFAULT_FROM_EMAIL, [email])
#         email_msg.attach("Event_Receipt.pdf", pdf_buffer.getvalue(), "application/pdf")
#         email_msg.send()

#         return JsonResponse({"success": True})
#     return JsonResponse({"success": False, "error": "Invalid request"}, status=400)


#payment
import razorpay
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

@csrf_exempt
def create_payment(request):
    if request.method == "POST":
        try:
            amount = request.POST.get("amount")
            if not amount or int(amount) <= 0:
                return JsonResponse({"error": "Invalid amount"}, status=400)

            amount = int(amount) * 100  # Convert to paisa

            # Create Razorpay order
            order_data = {
                "amount": amount,
                "currency": "INR",
                "payment_capture": 1,  # Auto capture payment
            }
            order = razorpay_client.order.create(order_data)

            return JsonResponse({
                "order_id": order["id"],
                "key": settings.RAZORPAY_KEY_ID
            })
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request"}, status=400)


@login_required
def confirm_order(request):
    if request.method == "POST":
        razorpay_payment_id = request.POST.get("razorpay_payment_id")
        total_amount = request.POST.get("total_amount")

        table_no =  request.POST.get("table_no")
        
        if not table_no:
            table_no = 9999
        print("table_no", table_no)
        
        if not razorpay_payment_id:
            return HttpResponse("Payment failed", status=400)

        user_profile = request.user
        cart_items = Cart.objects.filter(user=user_profile)

        if not cart_items:
            return HttpResponse("No items in cart", status=400)

        # Step 1: Create Order
        order = Order.objects.create(user=user_profile, total_amount=total_amount, table_no=table_no)

        # Step 2: Create OrderItems from Cart
        order_items = [
            OrderItem(order=order, food=item.food, quantity=item.quantity, price=item.food.price)
            for item in cart_items
        ]
        
        print(order_items)
        OrderItem.objects.bulk_create(order_items)  # Bulk insert for efficiency

        # Step 3: Clear the cart after checkout
        cart_items.delete()

        return redirect('order_success')  # Redirect to success page

    return HttpResponse("Invalid request", status=400)

@login_required
def order_success(request):
    return render(request, "order_success.html")

from datetime import date
from django.shortcuts import render
from .models import DiscountOffer

def discount_offers(request):
    today = date.today()
    offers = DiscountOffer.objects.filter(offer_end_date__gte=today)
    return render(request, 'Discount_&_offers.html', {'offers': offers})

@login_required(login_url='signin')
def feedback_view(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        feedback_text = request.POST.get('feedback')

        if name and email and feedback_text:
            # Save Feedback
            Feedback.objects.create(name=name, email=email, feedback=feedback_text)

            # Send Acknowledgment Email
            subject = "Feedback Acknowledgment - Malhar Exotica"
            message = f"Dear {name},\n\nThank you for submitting your feedback. We have received it and will get back to you soon if necessary.\n\nYour feedback:\n{feedback_text}\n\nBest Regards,\nMalhar Exotica Support Team"
            from_email = "malharexoticaa@gmail.com"  # Replace with your actual email
            recipient_list = [email]

            try:
                send_mail(subject, message, from_email, recipient_list, fail_silently=False)
                messages.success(request, "Your feedback has been submitted successfully, and an acknowledgment email has been sent.")
            except Exception as e:
                messages.error(request, "Feedback submitted, but failed to send acknowledgment email.")

            return redirect('feedback')  # Redirect after submission

    return render(request, 'feedback.html')

