from django.contrib import admin
from django.urls import path,include
from home import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('',views.home,name="home"),
    path('aboutus/',views.about,name="AboutUs"),
    path('team/',views.team,name="team"),
    path('testimonial/',views.testimonial,name="testimonial"),
    path('contact/',views.Contact,name="contact"),
    path('signin/',views.signin,name="signin"),
    path('admin_signin/', views.admin_signin, name='admin_signin'),  # Admin Login
    path('signup/',views.signup,name="signup"),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path("logout/", views.logout, name="logout"),
    path('prof', views.prof, name='prof'),
    path('editprofile/', views.edit_prof, name='edit_profile'),
    path('error/',views.errorpage,name='error'),

    # path('avltbl',views.get_available_tables,name='avltbl'),
    # path("book/", views.book_table, name="book_table"),
    # path("payment-success/", views.payment_success, name="payment_success"),
    
    path("book/", views.book_table, name="book_table"),
    path("payment-success/", views.payment_success, name="payment_success"),
    

    path('category/', views.category, name="category"),
    path('category/<str:category_name>/', views.sub_category, name="subcategory"),
    path('foodmenu/<str:subcategory_name>/', views.food_menu, name="foodmenu"),
    
    #cart and menu
    path('menu/', views.menu_view, name='menu_view'),
    path('add_to_cart/<int:food_id>/', views.add_to_cart, name='add_to_cart'),
    path('update_cart/<int:food_id>/<str:action>/', views.update_cart, name='update_cart'),
    path('cart/', views.cart_view, name='cart_view'),
    path("filter_menu/", views.filter_menu, name="filter_menu"),
    path('checkout/', views.checkout, name='checkout'),
    path('confirm-order/', views.confirm_order, name='confirm_order'), 
    path("order-success/", views.order_success, name="order_success"),
    path('discounts/', views.discount_offers, name='discount_offers'),

    path('events/', views.event_list, name='event_list'),  # List all events
    path('events/<int:event_id>/', views.event_details, name='event_details'),

    path('booking/<int:event_id>/<int:detail_id>/', views.event_booking, name='event_booking'),
    path('check-double-booking/', views.check_double_booking, name='check_double_booking'),
    path("send-booking-email/", views.send_booking_email, name="send_booking_email"),
    path("create-payment/", views.create_payment, name="create_payment"),

    path('feedback/', views.feedback_view, name='feedback'),

    # path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin/', admin.site.urls),
    
    #admindash
    path('adminlogin',views.admin_signin,name="adminsignin"),
    path('adminhome/',include('admin_panel.urls')),

]

from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
