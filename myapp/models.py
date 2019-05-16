from django.db import models
import datetime
from django.contrib.auth.models import User
from django.utils import timezone


class Category(models.Model):
    name = models.CharField(max_length=200)
    warehouse = models.CharField(max_length=200, blank=False, default='Windsor')


class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products',on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=100)
    available = models.BooleanField(default=True)
    description = models.TextField(blank=True, default='')


class Client(User):
    PROVINCE_CHOICES = [ ('AB', 'Alberta'), ('MB', 'Manitoba'), ('ON', 'Ontario'), ('QC', 'Quebec'),]
    company = models.CharField(max_length=50, blank=True, default='')
    shipping_address = models.CharField(max_length=300, null=True, blank=True)
    city = models.CharField(max_length=20, default='Windsor')
    province=models.CharField(max_length=2, choices=PROVINCE_CHOICES, default='ON')
    interested_in = models.ManyToManyField(Category)

class Order(models.Model):
    STATUS_CHOICES = [(0,'Order Cancelled'),(1, 'Order Placed'),(2, 'Order Shipped'),(3, 'Order Delivered')]
    product = models.ForeignKey(Product, related_name='orders',on_delete=models.CASCADE)
    client = models.ForeignKey( Client, related_name='orders', on_delete=models.CASCADE)
    num_units = models.PositiveIntegerField(default=100)
    order_status = models.IntegerField( choices=STATUS_CHOICES,default=1)
    status_date = models.DateField