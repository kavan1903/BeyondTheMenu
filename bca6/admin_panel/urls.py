
from django.urls import path,include
from admin_panel import views



urlpatterns = [
    path('', views.admin_dashboard, name='admin_dashboard'),
    path('categories/', views.manage_categories, name='manage_categories'),
    path('categories/add/', views.add_category, name='add_category'),
    path('categories/update/<int:category_id>/', views.update_category, name='update_category'),
    path('categories/delete/<int:category_id>/', views.delete_category, name='delete_category'),

    path('subcategories/', views.manage_subcategories, name='manage_subcategories'),
    path('subcategories/add/', views.add_subcategory, name='add_subcategory'),
    path('subcategories/update/<int:subcategory_id>/', views.update_subcategory, name='update_subcategory'),
    path('subcategories/delete/<int:subcategory_id>/', views.delete_subcategory, name='delete_subcategory'),

    path('adminmenu/', views.manage_menu, name='adminmenu_manage_menu'),
    path('adminmenu/add/', views.add_menu, name='adminmenu_add_menu'),
    path('adminmenu/update/<int:menu_id>/', views.update_menu, name='adminmenu_update_menu'),
    path('adminmenu/delete/<int:menu_id>/', views.delete_menu, name='adminmenu_delete_menu'),

    path('orders/', views.manage_orders, name='manage_orders'),
    path('orders/delete/<int:order_id>/', views.delete_order, name='delete_order'),

    path('tables/', views.manage_tables, name='manage_tables'),  # Manage all tables
    path('tables/add/', views.add_table, name='add_table'),  # Add a new table
    path('tables/update/<int:table_id>/', views.update_table, name='update_table'),  # Update table
    path('tables/delete/<int:table_id>/', views.delete_table, name='delete_table'),  # Delete table

    path('managebookings/', views.manage_bookings, name='manage_bookings'),
    path('managebookings/update/<int:booking_id>/', views.update_booking, name='update_booking'),
    path('managebookings/delete/<int:booking_id>/', views.delete_booking, name='delete_booking'),

    path('addevents/', views.manage_events, name='manage_events'),  # View all events
    path('addevents/add/', views.add_event, name='add_event'),  # Add new event
    path('addevents/update/<int:event_id>/', views.update_event, name='update_event'),  # Update event
    path('addevents/delete/<int:event_id>/', views.delete_event, name='delete_event'),  # Delete event

    path('event-details/manage/', views.manage_event_details, name='manage_event_details'),
    path('event-details/add/', views.add_event_detail, name='add_event_detail'),
    path('event-details/update/<int:detail_id>/', views.update_event_detail, name='update_event_detail'),
    path('event-details/delete/<int:detail_id>/', views.delete_event_detail, name='delete_event_detail'),

    path('manage-bookings/', views.manage_event_bookings, name='manage_event_bookings'),
    path('delete-booking/<int:booking_id>/', views.delete_event_booking, name='delete_event_booking'),

    path('discounts/', views.manage_discounts, name='manage_discounts'),
    path('discounts/add/', views.add_discount, name='add_discount'),
    path('discounts/update/<int:offer_id>/', views.update_discount, name='update_discount'),
    path('discounts/delete/<int:offer_id>/', views.delete_discount, name='delete_discount'),

    path('feedbacks/', views.manage_feedbacks, name='manage_feedbacks'),
    path('feedbacks/delete/<int:feedback_id>/', views.delete_feedback, name='delete_feedback'),


    path('users/', views.manage_users, name='manage_users'),
    path('users/add/', views.add_user, name='add_user'),
    path('users/update/<int:user_id>/', views.update_user, name='update_user'),
    path('users/delete/<int:user_id>/', views.delete_user, name='delete_user'),

    path('charts/', views.chart_view, name='charts'),
    path('charts/orders/', views.order_data, name='order_data'),
    path('charts/users/', views.user_registration_data, name='user_data'),
    path('charts/tables/', views.table_booking_data, name='table_booking_data'),
    path('charts/events/', views.event_booking_data, name='event_booking_data'),

    path('generate_report/', views.generate_report, name="generate_report"),
]

