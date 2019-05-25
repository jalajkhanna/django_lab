from django.shortcuts import render
from django.http import HttpResponse
from .models import Category,Product, Client, Order
from django.shortcuts import get_object_or_404, get_list_or_404

# Create your views here.
# def index(request):
#     return render(request, 'index.html')
# def about(request):
#     return render(request, 'about.html')
# def myaccount(request):
#     return render(request, 'myaccount.html')
# def purchase(request):
#     return render(request, 'purchase.html')
# def successorder(request):
#     return render(request, 'success.html')
# def clothing(request):
#     return render(request, 'clothing.html')
# def equipment(request):
#     return render(request, 'equipment.html')
# def otheritem(request):
#     return render(request, 'otheritem.html')
# def productdetails(request):
#     return render(request, 'productdetails.html')

def index(request):
    cat_list = Category.objects.all().order_by('id')[:10]
    product_list = Product.objects.all().order_by('-price')[:5]
    response = HttpResponse()
    heading1 = '<p>' + 'List of categories: ' + '</p>'
    response.write(heading1)
    for category in cat_list:
        para = '<p>' + str(category.id) + ': ' + str(category) + '</p>'
        response.write(para)
    heading2 = '<p>' + 'List of Products: ' + '</p>'
    response.write(heading2)
    for index,product in enumerate(product_list):
        p2 = '<p>' + str(index+1) + ':' + str(product) + '</p>'
        response.write(p2)

    return response

def about(request):
    response = HttpResponse()
    heading = '<h1>' + 'This is an Online Store App' + '</h1>'
    response.write(heading)
    return response


def cat_no(request, cat_no):
    warehouse_loc = get_list_or_404(Category.objects.filter(id=cat_no).values_list('warehouse'))
    prod_list = get_list_or_404(Product.objects.filter(category__id__contains=cat_no))
    response = HttpResponse()
    for location in warehouse_loc:
        para1 = '<p>' + 'Location of the  warehouse : ' + str(location[0]) + '</p>'
        response.write(para1)
    for index,products in enumerate(prod_list):
        para2 = '<p>' + 'Product ' + str(index+1) + ':' + str(products) + '</p>'
        response.write(para2)
    return response
