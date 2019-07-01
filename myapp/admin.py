from django.contrib import admin
from .models import Product, Category, Client, Order

# Register your models here.


def add_50_items(modeladmin, request, queryset):
    for product in queryset:
        product.stock+= 50
        product.save()
add_50_items.short_description = 'Add 50 items to stock'


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'available')
    actions = [add_50_items]


class ClientAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'city', 'categories_interested_in')

    def categories_interested_in(self,obj):
        return "\n".join([c.name for c in obj.interested_in.all()])


#register to admin
admin.site.register(Category)
admin.site.register(Order)
admin.site.register(Product, ProductAdmin)
admin.site.register(Client, ClientAdmin)
