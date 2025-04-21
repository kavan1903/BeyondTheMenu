import plotly.express as px
from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from home.models import MenuItem  # Import your model
from django.db.models import Count


@staff_member_required
def admin_dashboard(request):
    # Example: Count menu items per category
    category_data = MenuItem.objects.values('subcategory__name').annotate(count=Count('id'))

    
    # Convert data to a dictionary
    categories = [data['subcategory__name'] for data in category_data]
    counts = [data['count'] for data in category_data]

    # Create a bar chart
    fig = px.bar(x=categories, y=counts, labels={'x': 'Subcategories', 'y': 'Number of Items'}, title="Menu Items per Subcategory")
    chart = fig.to_html()

    return render(request, 'admin/custom_dashboard.html', {'chart': chart})
