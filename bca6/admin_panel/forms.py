from django import forms
from home.models import *  # Import the Category model from the home app
from django.contrib.auth.forms import UserCreationForm, UserChangeForm


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'image']  # Add all the fields you want to manage
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        } 

class SubcategoryForm(forms.ModelForm):
    class Meta:
        model = Subcategory
        fields = ['name', 'category', 'image']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter subcategory name'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

class MenuForm(forms.ModelForm):
    class Meta:
        model = Menu
        fields = ['name', 'subcategory', 'price', 'description', 'image']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter menu item name'}),
            'subcategory': forms.Select(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': 'Enter price'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enter description (optional)'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

    def clean_price(self):
        """ Ensure price is always positive """
        price = self.cleaned_data.get('price')
        if price and price <= 0:
            raise forms.ValidationError("Price must be greater than zero.")
        return price

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['user', 'total_amount']
        widgets = {
            'user': forms.Select(attrs={'class': 'form-control'}),
            'total_amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }

class TableForm(forms.ModelForm):
    class Meta:
        model = Manage_Table
        fields = ['table_number', 'capacity', 'is_occupied']
        widgets = {
            'table_number': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter table number'}),
            'capacity': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter seating capacity'}),
            'is_occupied': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
    labels = {
        'table_number': 'Table Number',
        'capacity': 'Seating Capacity',
        'is_occupied': 'Occupied',
    }


class TableBookingForm(forms.ModelForm):
    booking_time = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
        label="Booking Time"
    )

    class Meta:
        model = TableBooking
        fields = ['name', 'phone', 'email', 'num_people', 'num_tables', 'booking_time', 'status']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'num_people': forms.NumberInput(attrs={'class': 'form-control'}),
            'num_tables': forms.NumberInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['name', 'description', 'image', 'location']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter event name'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Enter event description'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter event location'}),
        }

class EventDetailsForm(forms.ModelForm):
    class Meta:
        model = EventDetails
        fields = ['event', 'name', 'long_description', 'additional_images', 'charge']
        widgets = {
            'event': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'long_description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'additional_images': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'charge': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }


class EventBookingForm(forms.ModelForm):
    class Meta:
        model = EventBooking
        fields = ['event', 'name', 'email', 'date', 'time', 'no_of_persons', 'advance_charges']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'no_of_persons': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'advance_charges': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }

class DiscountOfferForm(forms.ModelForm):
    class Meta:
        model = DiscountOffer
        fields = ['offer_start_date', 'offer_end_date', 'offer_desc', 'discount_percentage']
        widgets = {
            'offer_start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'offer_end_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'offer_desc': forms.TextInput(attrs={'class': 'form-control', 'maxlength': '35'}),
            'discount_percentage': forms.NumberInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        today = date.today().strftime('%Y-%m-%d')
        self.fields['offer_start_date'].widget.attrs['min'] = today
        self.fields['offer_end_date'].widget.attrs['min'] = today


class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['name', 'email', 'feedback']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email'}),
            'complaint': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Write your feedback here...', 'rows': 4}),
        }


class UserProfileCreationForm(UserCreationForm):
    class Meta:
        model = UserProfile
        fields = ['name', 'email', 'phone', 'gender', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(UserProfileCreationForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter full name'})
        self.fields['email'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter email'})
        self.fields['phone'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter phone number'})
        self.fields['gender'].widget.attrs.update({'class': 'form-control'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter password'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Confirm password'})

class UserProfileUpdateForm(UserChangeForm):
    password = None  # Exclude password field

    class Meta:
        model = UserProfile
        fields = ['name', 'email', 'phone', 'gender']

    def __init__(self, *args, **kwargs):
        super(UserProfileUpdateForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter full name'})
        self.fields['email'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter email'})
        self.fields['phone'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter phone number'})
        self.fields['gender'].widget.attrs.update({'class': 'form-control'})