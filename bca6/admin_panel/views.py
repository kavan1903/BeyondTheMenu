from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import *
from django.db.models import Sum,Count
from .forms import * # Import the form
from django.core.paginator import Paginator  # For pagination
import json
from django.http import JsonResponse

import json
from decimal import Decimal
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count
from django.shortcuts import render
from django.utils.timezone import now
from home.models import Order, Menu, EventBooking  # Removed TableBooking

UserProfile = get_user_model()

@login_required
def admin_dashboard(request):
    total_orders = Order.objects.count()
    total_menu_items = Menu.objects.count()
    total_sales = Order.objects.aggregate(Sum('total_amount'))['total_amount__sum'] or Decimal(0)
    total_users = UserProfile.objects.count()

    # Get today's date
    today = now().date()

    # Fetch daily revenue (sales for today only)
    today_sales = (
        Order.objects.filter(created_at__date=today)
        .aggregate(Sum('total_amount'))['total_amount__sum']
    ) or Decimal(0)

    # Order Sales Data (Daily Sales) - Revenue generated per day based on placed orders
    order_data = (
        Order.objects.values('created_at__date')
        .annotate(
            total_sales=Sum('total_amount'),  # Sum of total revenue for each day
            order_count=Count('id')  # Count of total orders placed per day
        )
        .order_by('created_at__date')
    )

    # Labels: Date when orders were placed
    order_labels = [str(order['created_at__date']) for order in order_data]

    # Values: Revenue generated on each day based on actual placed orders
    order_values = [float(order['total_sales']) for order in order_data]

    # Order Count: Total number of orders placed on each date
    order_counts = [order['order_count'] for order in order_data]

    # Event Bookings Data
    event_booking_data = (
        EventBooking.objects.values('date', 'event__name')
        .annotate(total_bookings=Count('id'))
        .order_by('date')
    )
    event_labels = [f"{booking['event__name']} ({booking['date']})" for booking in event_booking_data]
    event_values = [booking['total_bookings'] for booking in event_booking_data]

    # Top-Selling Food Items
    top_selling_food = (
        Menu.objects.annotate(total_sold=Count('orderitem'))
        .order_by('-total_sold')[:5]
    )
    top_food_labels = [item.name for item in top_selling_food]
    top_food_values = [item.total_sold for item in top_selling_food]

    context = {
        'total_orders': total_orders,
        'total_menu_items': total_menu_items,
        'total_sales': f"₹{float(total_sales):,.2f}",
        'total_users': total_users,
        'daily_revenue': f"₹{float(today_sales):,.2f}",  # Send today's revenue to the template

        'order_labels': json.dumps(order_labels) if order_labels else json.dumps([]),
        'order_values': json.dumps(order_values) if order_values else json.dumps([]),
        'order_counts': json.dumps(order_counts) if order_counts else json.dumps([]),

        'event_labels': json.dumps(event_labels) if event_labels else json.dumps([]),
        'event_values': json.dumps(event_values) if event_values else json.dumps([]),

        'top_food_labels': json.dumps(top_food_labels) if top_food_labels else json.dumps([]),
        'top_food_values': json.dumps(top_food_values) if top_food_values else json.dumps([]),
    }

    return render(request, 'admin/dashboard.html', context)

@login_required
def manage_categories(request):
    categories = Category.objects.all()
    paginator = Paginator(categories, 10)  # Show 10 categories per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'admin/manage_categories.html', {'page_obj': page_obj})

# Add Category
@login_required
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Category added successfully!")  # Success message
            return redirect('manage_categories')
        else:
            messages.error(request, "Failed to add category. Please check the form.")  # Error message
    else:
        form = CategoryForm()
    return render(request, 'admin/add_category.html', {'form': form})

# Update Category
@login_required
def update_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, "Category updated successfully!")  # Success message
            return redirect('manage_categories')
        else:
            messages.error(request, "Failed to update category. Please check the form.")  # Error message
    else:
        form = CategoryForm(instance=category)
    return render(request, 'admin/update_category.html', {'form': form, 'category': category})

# Delete Category
@login_required
def delete_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    if request.method == 'POST':
        category.delete()
        messages.success(request, "Category deleted successfully!")  # Success message
        return redirect('manage_categories')
    return render(request, 'admin/delete_category.html', {'category': category})


@login_required
def manage_subcategories(request):
    subcategories = Subcategory.objects.all()
    paginator = Paginator(subcategories, 10)  # Show 10 subcategories per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'admin/manage_subcategories.html', {'page_obj': page_obj})

# Add Subcategory
@login_required
def add_subcategory(request):
    if request.method == 'POST':
        form = SubcategoryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Subcategory added successfully!")  # Success message
            return redirect('manage_subcategories')
        else:
            messages.error(request, "Failed to add subcategory. Please check the form.")  # Error message
    else:
        form = SubcategoryForm()
    return render(request, 'admin/add_subcategory.html', {'form': form})

# Update Subcategory
@login_required
def update_subcategory(request, subcategory_id):
    subcategory = get_object_or_404(Subcategory, id=subcategory_id)
    if request.method == 'POST':
        form = SubcategoryForm(request.POST, request.FILES, instance=subcategory)
        if form.is_valid():
            form.save()
            messages.success(request, "Subcategory updated successfully!")  # Success message
            return redirect('manage_subcategories')
        else:
            messages.error(request, "Failed to update subcategory. Please check the form.")  # Error message
    else:
        form = SubcategoryForm(instance=subcategory)
    return render(request, 'admin/update_subcategory.html', {'form': form, 'subcategory': subcategory})

# Delete Subcategory
@login_required
def delete_subcategory(request, subcategory_id):
    subcategory = get_object_or_404(Subcategory, id=subcategory_id)
    if request.method == 'POST':
        subcategory.delete()
        messages.success(request, "Subcategory deleted successfully!")  # Success message
        return redirect('manage_subcategories')
    return render(request, 'admin/delete_subcategory.html', {'subcategory': subcategory})


@login_required
def manage_menu(request):
    menu_items = Menu.objects.all()
    paginator = Paginator(menu_items, 10)  # Show 10 menu items per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'admin/manage_menu.html', {'page_obj': page_obj})

# Add Menu Item
@login_required
def add_menu(request):
    if request.method == 'POST':
        form = MenuForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Menu item added successfully!")  # Success message
            return redirect('adminmenu_manage_menu')
        else:
            messages.error(request, "Failed to add menu item. Please check the form.")  # Error message
    else:
        form = MenuForm()
    return render(request, 'admin/add_menu.html', {'form': form})

# Update Menu Item
@login_required
def update_menu(request, menu_id):
    menu_item = get_object_or_404(Menu, id=menu_id)
    if request.method == 'POST':
        form = MenuForm(request.POST, request.FILES, instance=menu_item)
        if form.is_valid():
            form.save()
            messages.success(request, "Menu item updated successfully!")  # Success message
            return redirect('adminmenu_manage_menu')
        else:
            messages.error(request, "Failed to update menu item. Please check the form.")  # Error message
    else:
        form = MenuForm(instance=menu_item)
    return render(request, 'admin/update_menu.html', {'form': form, 'menu_item': menu_item})

# Delete Menu Item
@login_required
def delete_menu(request, menu_id):
    menu_item = get_object_or_404(Menu, id=menu_id)
    if request.method == 'POST':
        menu_item.delete()
        messages.success(request, "Menu item deleted successfully!")  # Success message
        return redirect('adminmenu_manage_menu')
    return render(request, 'admin/delete_menu.html', {'menu_item': menu_item})


def manage_orders(request):
    orders = Order.objects.all()
    
    # Use select_related to avoid extra DB queries
    order_items_qs = OrderItem.objects.select_related('food').all()
    
    # Build custom list with food name instead of food ID
    orderItems = [
        {
            "order": item.order.id,
            "food": item.food.name,
            "quantity": item.quantity
        }
        for item in order_items_qs
    ]

    print(orderItems)  # Now food names will show

    return render(request, 'admin/manage_orders.html', {
        'orders': orders,
        'orderItems': orderItems
    })



def delete_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if request.method == 'POST':
        order.delete()
        messages.success(request, "Order deleted successfully!")
        return redirect('manage_orders')
    return render(request, 'admin/delete_order.html', {'order': order})


def manage_tables(request):
    tables = Manage_Table.objects.all()
    return render(request, 'admin/manage_tables.html', {'tables': tables})

def add_table(request):
    if request.method == "POST":
        form = TableForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Table added successfully!")
            return redirect('manage_tables')
    else:
        form = TableForm()
    return render(request, 'admin/add_table.html', {'form': form})

def update_table(request, table_id):
    table = get_object_or_404(Manage_Table, id=table_id)
    if request.method == "POST":
        form = TableForm(request.POST, instance=table)
        if form.is_valid():
            form.save()
            messages.success(request, "Table updated successfully!")
            return redirect('manage_tables')
    else:
        form = TableForm(instance=table)
    return render(request, 'admin/update_table.html', {'form': form, 'table': table})

def delete_table(request, table_id):
    table = get_object_or_404(Manage_Table, id=table_id)
    if request.method == "POST":
        table.delete()
        messages.success(request, "Table deleted successfully!")
        return redirect('manage_tables')
    return render(request, 'admin/delete_table.html', {'table': table})


def manage_bookings(request):
    bookings = TableBooking.objects.all()
    return render(request, 'admin/manage_bookings.html', {'bookings': bookings})

# Update booking
def update_booking(request, booking_id):
    booking = get_object_or_404(TableBooking, id=booking_id)
    if request.method == 'POST':
        form = TableBookingForm(request.POST, instance=booking)
        if form.is_valid():
            form.save()
            messages.success(request, "Booking updated successfully!")
            return redirect('manage_bookings')
    else:
        form = TableBookingForm(instance=booking)
    return render(request, 'admin/update_booking.html', {'form': form, 'booking': booking})

# Delete booking
def delete_booking(request, booking_id):
    booking = get_object_or_404(TableBooking, id=booking_id)
    if request.method == "POST":
        booking.delete()
        messages.success(request, "Booking deleted successfully!")
        return redirect('manage_bookings')
    return render(request, 'admin/delete_booking.html', {'booking': booking})

# Manage Events
def manage_events(request):
    events = Event.objects.all()
    return render(request, 'admin/manage_events.html', {'events': events})

# Add Event
def add_event(request):
    if request.method == "POST":
        form = EventForm(request.POST, request.FILES)  # Handle image upload
        if form.is_valid():
            form.save()
            messages.success(request, "Event added successfully!")
            return redirect('manage_events')
    else:
        form = EventForm()
    return render(request, 'admin/add_event.html', {'form': form})

# Update Event
def update_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if request.method == "POST":
        form = EventForm(request.POST, request.FILES, instance=event)  # Handle image upload
        if form.is_valid():
            form.save()
            messages.success(request, "Event updated successfully!")
            return redirect('manage_events')
    else:
        form = EventForm(instance=event)
    return render(request, 'admin/update_event.html', {'form': form, 'event': event})

# Delete Event
def delete_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if request.method == "POST":
        event.delete()
        messages.success(request, "Event deleted successfully!")
        return redirect('manage_events')
    return render(request, 'admin/delete_event.html', {'event': event})


def manage_event_details(request):
    event_details = EventDetails.objects.all()
    return render(request, 'admin/manage_event_details.html', {'event_details': event_details})

def add_event_detail(request):
    if request.method == "POST":
        form = EventDetailsForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Event details added successfully!")
            return redirect('manage_event_details')
    else:
        form = EventDetailsForm()
    return render(request, 'admin/add_event_detail.html', {'form': form})

def update_event_detail(request, detail_id):
    event_detail = get_object_or_404(EventDetails, id=detail_id)
    if request.method == "POST":
        form = EventDetailsForm(request.POST, request.FILES, instance=event_detail)
        if form.is_valid():
            form.save()
            messages.success(request, "Event details updated successfully!")
            return redirect('manage_event_details')
    else:
        form = EventDetailsForm(instance=event_detail)
    return render(request, 'admin/update_event_detail.html', {'form': form, 'event_detail': event_detail})

def delete_event_detail(request, detail_id):
    event_detail = get_object_or_404(EventDetails, id=detail_id)
    if request.method == "POST":
        event_detail.delete()
        messages.success(request, "Event details deleted successfully!")
        return redirect('manage_event_details')
    return render(request, 'admin/delete_event_detail.html', {'event_detail': event_detail})


def manage_event_bookings(request):
    bookings = EventBooking.objects.all()
    return render(request, 'admin/manage_event_bookings.html', {'bookings': bookings})

def delete_event_booking(request, booking_id):
    booking = get_object_or_404(EventBooking, id=booking_id)
    if request.method == "POST":
        booking.delete()
        messages.success(request, "Event booking deleted successfully!")
        return redirect('manage_event_bookings')
    return render(request, 'admin/delete_event_booking.html', {'booking': booking})


def manage_discounts(request):
    discounts = DiscountOffer.objects.all()
    return render(request, 'admin/manage_discounts.html', {'discounts': discounts})

# Add Discount Offer
def add_discount(request):
    if request.method == "POST":
        form = DiscountOfferForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Discount Offer added successfully!")
            return redirect('manage_discounts')
    else:
        form = DiscountOfferForm()
    return render(request, 'admin/add_discount.html', {'form': form})

# Update Discount Offer
def update_discount(request, offer_id):
    discount = get_object_or_404(DiscountOffer, offer_id=offer_id)
    if request.method == "POST":
        form = DiscountOfferForm(request.POST, instance=discount)
        if form.is_valid():
            form.save()
            messages.success(request, "Discount Offer updated successfully!")
            return redirect('manage_discounts')
    else:
        form = DiscountOfferForm(instance=discount)
    return render(request, 'admin/update_discount.html', {'form': form, 'discount': discount})

# Delete Discount Offer
def delete_discount(request, offer_id):
    discount = get_object_or_404(DiscountOffer, offer_id=offer_id)
    if request.method == "POST":
        discount.delete()
        messages.success(request, "Discount Offer deleted successfully!")
        return redirect('manage_discounts')
    return render(request, 'admin/delete_discount.html', {'discount': discount})


# View to manage feedbacks
def manage_feedbacks(request):
    feedbacks = Feedback.objects.all().order_by('-submitted_at')
    return render(request, 'admin/manage_feedbacks.html', {'feedbacks': feedbacks})

# View to delete a feedback
def delete_feedback(request, feedback_id):
    feedback = get_object_or_404(Feedback, id=feedback_id)
    if request.method == "POST":
        feedback.delete()
        messages.success(request, "Feedback deleted successfully!")
        return redirect('manage_feedbacks')
    return render(request, 'admin/delete_feedback.html', {'feedback': feedback})




@login_required
def manage_users(request):
    users = UserProfile.objects.all()
    return render(request, 'admin/manage_users.html', {'users': users})

# Add a new user
@login_required
def add_user(request):
    if request.method == "POST":
        form = UserProfileCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "User added successfully!")
            return redirect('manage_users')
    else:
        form = UserProfileCreationForm()
    return render(request, 'admin/add_user.html', {'form': form})

# Update user details
@login_required
def update_user(request, user_id):
    user = get_object_or_404(UserProfile, id=user_id)
    if request.method == "POST":
        form = UserProfileUpdateForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "User updated successfully!")
            return redirect('manage_users')
    else:
        form = UserProfileUpdateForm(instance=user)
    return render(request, 'admin/update_user.html', {'form': form, 'user': user})

# Delete user
@login_required
def delete_user(request, user_id):
    user = get_object_or_404(UserProfile, id=user_id)
    if request.method == "POST":
        user.delete()
        messages.success(request, "User deleted successfully!")
        return redirect('manage_users')
    return render(request, 'admin/delete_user.html', {'user': user})

def order_data(request):
    """Returns order data for charts."""
    orders = Order.objects.values('created_at__date').annotate(total_sales=Sum('total_amount')).order_by('created_at__date')
    data = {
        'labels': [str(order['created_at__date']) for order in orders],
        'values': [order['total_sales'] for order in orders],
    }
    return JsonResponse(data)

def user_registration_data(request):
    """Returns user registration data."""
    users = UserProfile.objects.values('date_joined__date').annotate(total_users=Count('id')).order_by('date_joined__date')
    data = {
        'labels': [str(user['date_joined__date']) for user in users],
        'values': [user['total_users'] for user in users],
    }
    return JsonResponse(data)

def table_booking_data(request):
    """Returns table booking data."""
    bookings = TableBooking.objects.values('booking_time__date').annotate(total_bookings=Count('id')).order_by('booking_time__date')
    data = {
        'labels': [str(booking['booking_time__date']) for booking in bookings],
        'values': [booking['total_bookings'] for booking in bookings],
    }
    return JsonResponse(data)

def event_booking_data(request):
    """Returns event booking data."""
    bookings = EventBooking.objects.values('date').annotate(total_bookings=Count('id')).order_by('date')
    data = {
        'labels': [str(booking['date']) for booking in bookings],
        'values': [booking['total_bookings'] for booking in bookings],
    }
    return JsonResponse(data)

def chart_view(request):
    """Render the chart template."""
    return render(request, 'dashboard.html')

from django.http import HttpResponse
from django.shortcuts import render
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors
from .models import *
from datetime import datetime

def generate_report(request):
    if request.method == "POST":
        report_type = request.POST.get("report_type")
        start_date = request.POST.get("start_date")
        end_date = request.POST.get("end_date")

        # Convert string date to datetime objects
        start_date = datetime.strptime(start_date, "%Y-%m-%d")
        end_date = datetime.strptime(end_date, "%Y-%m-%d")

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{report_type}_{start_date.date()}_to_{end_date.date()}.pdf"'

        pdf = canvas.Canvas(response, pagesize=letter)
        pdf.setTitle(f"{report_type.capitalize()} Report - {start_date.date()} to {end_date.date()}")

        # **Add Company Name**
        pdf.setFont("Helvetica-Bold", 16)
        pdf.drawString(200, 780, "Malhar Exotica")  # Company Name

        # **Report Title**
        pdf.setFont("Helvetica-Bold", 14)
        pdf.drawString(200, 750, f"{report_type.capitalize()} Report")

        # **Date Range**
        pdf.setFont("Helvetica", 12)
        pdf.drawString(200, 730, f"Date Range: {start_date.date()} to {end_date.date()}")

        data = []
        if report_type == "sales":
            data.append(["Order ID", "Customer", "Total Amount", "Date"])
            
            # Corrected Query: Use `created_at__range`
            orders = Order.objects.filter(created_at__range=[start_date, end_date])

            for order in orders:
                data.append([order.id, order.user.email, f"rs.{order.total_amount}", order.created_at.strftime("%Y-%m-%d")])

        elif report_type == "table_booking":
            data.append(["Booking ID", "Customer", "Table Number", "Date"])
            bookings = TableBooking.objects.filter(
                booking_time__date__range=[start_date.date(), end_date.date()]
            )
            for booking in bookings:
                data.append([
                    booking.id,
                    booking.name,
                    booking.num_tables,
                    booking.booking_time.strftime("%Y-%m-%d %H:%M")
                ])


        elif report_type == "event_booking":
            data.append(["Event ID", "Customer", "Event Name", "Date", "Email"])
            events = EventBooking.objects.filter(date__range=[start_date, end_date])
            for event in events:
                data.append([event.id, event.name, event.event.name, str(event.date), event.email])
        if len(data) > 1:
            table = Table(data)  # ✅ Fixed this line
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))

            table.wrapOn(pdf, 500, 600)
            table.drawOn(pdf, 50, 600 - (len(data) * 20))
        else:
            pdf.drawString(200, 700, "No data available for the selected date range.")


        pdf.save()
        return response

    return render(request, "admin/generate_report.html")
