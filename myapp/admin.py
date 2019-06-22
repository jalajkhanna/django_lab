from django.contrib import admin
from .models import Product, Category, Client, Order

# Register your models here.

admin.site.register(Category)
admin.site.register(Client)
admin.site.register(Order)


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'available')
admin.site.register(Product, ProductAdmin)




