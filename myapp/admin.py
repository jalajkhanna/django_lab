from django.contrib import admin
from .models import Product, Category, Client, Order

# Register your models here.

admin.site.register(Category)
admin.site.register(Client)
admin.site.register(Order)


def add_50_items(modeladmin, request, queryset):
    for product in queryset:
        product.stock+= 50
        product.save()
add_50_items.short_description = 'Add 50 items to stock'


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'available')
    actions = [add_50_items,]
admin.site.register(Product, ProductAdmin)





