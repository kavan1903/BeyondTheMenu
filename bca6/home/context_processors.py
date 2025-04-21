from django.db.models import Sum
from .models import Cart  # Import your Cart model

def cart_count(request):
    if request.user.is_authenticated:
        count = Cart.objects.filter(user=request.user).aggregate(total_items=Sum('quantity'))['total_items'] or 0
    else:
        count = 0
    return {"cart_count":count}