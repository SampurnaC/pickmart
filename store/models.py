from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Category(models.Model):
    name=models.CharField(max_length=100)
    description=models.TextField()

    def __str__(self):
        return self.name
    
class Product(models.Model):
    name=models.CharField(max_length=200)
    description=models.TextField()
    price=models.DecimalField(max_digits=10, decimal_places=2)
    stock=models.PositiveIntegerField()
    image=models.ImageField(upload_to='products/', blank=True, null=True)
    
    def __str__(self):
        return self.name

class Order(models.Model):
    customer=models.ForeignKey(User, on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    is_paid=models.BooleanField(default=False)
    
    def __str__(self):
        return f"Order {self.id} by {self.customer}"
    
class OrderItem(models.Model):
    order=models.ForeignKey(Order, on_delete=models.CASCADE)
    product=models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField(default=1)
    
    def __str__(self):
        return f"{self.quantity} of {self.product.name}"

