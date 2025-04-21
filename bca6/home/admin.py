from django.contrib import admin
from django.utils.html import format_html
from .models import *

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'gender')
    search_fields = ('name', 'email', 'phone')
    ordering = ('id',) 

admin.site.register(UserProfile, UserProfileAdmin)

# class BookingAdmin(admin.ModelAdmin):
#     list_display = ('name', 'email', 'date_time', 'no_of_people', 'created_at')
#     search_fields = ('name', 'email')
#     list_filter = ('date_time',)
#     ordering = ('id',)

#     def has_add_permission(self, request):
#         return False 

# admin.site.register(Booking, BookingAdmin)

@admin.register(TableBooking)
class TableBookingAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'num_people', 'num_tables', 'booking_time', 'status')
    list_filter = ('status', 'booking_time')
    search_fields = ('name', 'phone', 'email')
    ordering = ('-booking_time',)
    list_editable = ('status',)  # Allow quick status updates
    
    def has_add_permission(self, request):
        return True  # Allow adding new bookings manually

    def has_change_permission(self, request, obj=None):
        return True  # Allow editing existing bookings

    def has_delete_permission(self, request, obj=None):
        return True  # Allow deleting bookings

@admin.register(BookingSlot)
class BookingSlotAdmin(admin.ModelAdmin):
    list_display = ('slot_time', 'available_tables')
    list_filter = ('slot_time',)
    list_editable = ('available_tables',)  # Allow updating available tables directly
    ordering = ('slot_time',)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    ordering = ('id',)  # Added ordering

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="80" height="80" style="border-radius: 5px;" />', obj.image.url)
        return "No Image"

    image_preview.short_description = "Image Preview"

admin.site.register(Category, CategoryAdmin)

class SubcategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "category")
    search_fields = ("name", "category__name")
    fields = ("name", "category", "image")
    ordering = ('id',)  # Added ordering

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="80" height="80" style="border-radius: 5px;" />', obj.image.url)
        return "No Image"

    image_preview.short_description = "Image Preview"

admin.site.register(Subcategory, SubcategoryAdmin)

class MenuAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "subcategory", "price", "created_at", "updated_at", "image_preview")
    search_fields = ("name", "subcategory__name")
    ordering = ('id',)  # Added ordering

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" style="border-radius:5px;"/>', obj.image.url)
        return "No Image"

    image_preview.short_description = "Image Preview"

admin.site.register(Menu, MenuAdmin)

class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'food', 'quantity')
    list_filter = ('user',)
    search_fields = ('user__username', 'food__name')
    ordering = ('id',)  
    def has_add_permission(self, request):
        return False  # Prevents admin from adding cart items

admin.site.register(Cart, CartAdmin)


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("name", "location", "event_image")  # Show image in list display

    def event_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" style="border-radius: 5px;"/>', obj.image.url)
        return "No Image"
    event_image.allow_tags = True
    event_image.short_description = "Image"

@admin.register(EventDetails)
class EventDetailsAdmin(admin.ModelAdmin):
    list_display = ("event", "name", "charge", "details_image")  # Show image in list display
    search_fields = ("event__name",)  # Allow searching by event name

    def details_image(self, obj):
        if obj.additional_images:
            return format_html('<img src="{}" width="50" height="50" style="border-radius: 5px;"/>', obj.additional_images.url)
        return "No Image"
    details_image.allow_tags = True
    details_image.short_description = "Image"



class EventBookingAdmin(admin.ModelAdmin):
    list_display = ('name', 'event', 'email', 'date', 'time', 'no_of_persons', 'advance_charges')
    list_filter = ('event', 'date')
    search_fields = ('name', 'email', 'event__name')

    def has_add_permission(self, request):
        return False  # Disables the 'Add' button in admin

admin.site.register(EventBooking, EventBookingAdmin)

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0  # Prevent extra empty fields
    readonly_fields = ('food', 'quantity', 'price')  # Prevent editing checked-out items


class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'total_amount', 'created_at', 'table_no')
    inlines = [OrderItemInline]  # Show order items inside order details
    search_fields = ('user__name', 'user__email')
    list_filter = ('created_at',)
    readonly_fields = ('total_amount', 'created_at', 'table_no')  # Ensure total amount is not edited manually
    ordering=('id',)

    def has_add_permission(self, request):
        return False

admin.site.register(Order, OrderAdmin)

@admin.register(Manage_Table)
class TableAdmin(admin.ModelAdmin):
    list_display = ("table_number", "capacity", "is_occupied")
    list_filter = ("is_occupied", "capacity")
    search_fields = ("table_number",)
    ordering = ("table_number",)

    def mark_as_available(self, request, queryset):
        queryset.update(is_occupied=False)
    mark_as_available.short_description = "Mark selected tables as available"

    actions = [mark_as_available]

@admin.register(DiscountOffer)
class DiscountOfferAdmin(admin.ModelAdmin):
    list_display = ('offer_id', 'offer_desc', 'discount_percentage', 'offer_start_date', 'offer_end_date')
    search_fields = ('offer_desc',)
    list_filter = ('offer_start_date', 'offer_end_date')

    actions = ['delete_expired_offers']

    def delete_expired_offers(self, request, queryset):
        queryset.filter(offer_end_date__lt=date.today()).delete()
    delete_expired_offers.short_description = "Delete expired offers"

class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'submitted_at')  # Fields to show in the admin panel
    search_fields = ('name', 'email', 'feedback')  # Enable search
    list_filter = ('submitted_at',)  # Filter by date

    def has_add_permission(self, request):
        return False
admin.site.register(Feedback, FeedbackAdmin)


from django.contrib import admin
from .models import Cart

class CartAdmin(admin.ModelAdmin):
    def has_view_permission(self, request, obj=None):
        """Restrict superuser from viewing Cart"""
        if request.user.is_superuser:
            return False
        return True  # Allow other users

    def has_change_permission(self, request, obj=None):
        """Restrict superuser from editing Cart"""
        if request.user.is_superuser:
            return False
        return True

    def has_add_permission(self, request):
        """Restrict superuser from adding items to Cart"""
        if request.user.is_superuser:
            return False
        return True

    def has_delete_permission(self, request, obj=None):
        """Restrict superuser from deleting Cart"""
        if request.user.is_superuser:
            return False
        return True

    def has_module_permission(self, request):
        """Hide Cart from the admin panel for superusers"""
        if request.user.is_superuser:
            return False
        return True  # Allow access for other staff users

# Unregister the Cart model first if it is already registered
admin.site.unregister(Cart)
admin.site.register(Cart,CartAdmin)