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
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to="food_images/", blank=True, null=True)  # ImageField for file upload
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

#cart
class Cart(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    food = models.ForeignKey('Menu', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.food.name} - {self.user.email}"