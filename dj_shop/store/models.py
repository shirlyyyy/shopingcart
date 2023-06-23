from django.db import models
from django.contrib.auth.models import User
import uuid

class Product(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=255, default='')
    price = models.IntegerField()
    picture = models.ImageField(upload_to="img", default="")

    def __str__(self):
        return self.name
    
class Cart(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)
    
    def __str__(self):
        return str(self.id)
    
    @property
    def total_price(self):
        total = sum([item.product.price * item.quantity for item in self.cartitems.all()])
        return total    
    
    @property
    def num_of_items(self):
        quantity = sum([item.quantity for item in self.cartitems.all()])
        return quantity

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cartitems')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='cartitems')
    quantity = models.IntegerField(default=0)

    def __str__(self):
        return self.product.name
    
    @property
    def price(self):
        return self.product.price * self.quantity
    
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} - {self.user.username}"

    @property
    def total_price(self):
        total = sum([item.price for item in self.order_items.all()])
        return total

    @property
    def num_of_items(self):
        quantity = sum([item.quantity for item in self.order_items.all()])
        return quantity

class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    quantity = models.IntegerField(default=0)

    def __str__(self):
        return f"OrderItem #{self.id} - {self.product.name}"

    @property
    def price(self):
        return self.product.price * self.quantity
