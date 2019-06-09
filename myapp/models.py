from django.db import models
import datetime
from django.contrib.auth.models import User
from django.utils import timezone
from django.forms import ModelForm


class Category(models.Model):
    name = models.CharField(max_length=200)
    warehouse = models.CharField(max_length=200, blank=False, default='Windsor')
    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products',on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=100)
    available = models.BooleanField(default=True)
    description = models.TextField(blank=True, default='')
    interested = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name

    def refill(self):
        return self.stock+100

    def updateStock(self,var,newstock,num):
        Product.objects.filter(name=var).update(stock=newstock-num)
        return self.stock


class Client(User):
    PROVINCE_CHOICES = [ ('AB', 'Alberta'), ('MB', 'Manitoba'), ('ON', 'Ontario'), ('QC', 'Quebec'),]
    company = models.CharField(max_length=50, blank=True, default='')
    shipping_address = models.CharField(max_length=300, null=True, blank=True)
    city = models.CharField(max_length=20, default='Windsor')
    province=models.CharField(max_length=2, choices=PROVINCE_CHOICES, default='ON')
    interested_in = models.ManyToManyField(Category)

    def __str__(self):
        result = User.get_full_name(self)
        return result

class Order(models.Model):
    STATUS_CHOICES = [(0,'Order Cancelled'),(1, 'Order Placed'),(2, 'Order Shipped'),(3, 'Order Delivered')]
    product = models.ForeignKey(Product, related_name='orders',on_delete=models.CASCADE)
    client = models.ForeignKey( Client, related_name='orders', on_delete=models.CASCADE)
    num_units = models.PositiveIntegerField(default=100)
    order_status = models.IntegerField( choices=STATUS_CHOICES,default=1)
    status_date = models.DateField(default=datetime.date.today)

    def __str__(self):
        result = str(self.client)+str(self.product)+'-'+str(self.num_units)+'on'+str(self.status_date)
        return result

    def total_cost(self):
        total = (self.product.price)*(self.num_units)
        return total


class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = ['client','product','num_units']