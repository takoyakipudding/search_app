from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from django.db import models

class Category(models.Model): 
    name = models.CharField(max_length=255) 
 
    def __str__(self): 
        return self.name 
 
class Product(models.Model): 
    name = models.CharField(max_length=255) 
    description = models.TextField() 
    price = models.IntegerField()  
    category = models.ForeignKey(Category, on_delete=models.CASCADE) 
 
    def __str__(self): 
        return str(_(self.name))

class SearchHistory(models.Model):
    query = models.CharField(max_length=255)
    search_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.query

class SearchSettings(models.Model):
    search_type = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.search_type

class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.product.name} ({self.quantity})"
