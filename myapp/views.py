from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.utils.datetime_safe import datetime

from .models import Category, Product, Client, Order
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import get_object_or_404, get_list_or_404
from myapp.forms import OrderForm, InterestForm, LoginForm
from django.urls import reverse


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
#
# def index(request):
#     cat_list = Category.objects.all().order_by('id')[:10]
#     product_list = Product.objects.all().order_by('-price')[:5]
#     response = HttpResponse()
#     heading1 = '<p>' + 'List of categories: ' + '</p>'
#     response.write(heading1)
#     for category in cat_list:
#         para = '<p>' + str(category.id) + ': ' + str(category) + '</p>'
#         response.write(para)
#     heading2 = '<p>' + 'List of Products: ' + '</p>'
#     response.write(heading2)
#     for index,product in enumerate(product_list):
#         p2 = '<p>' + str(index+1) + ':' + str(product) + '</p>'
#         response.write(p2)
#
#     return response


def index(request):
    cat_list = Category.objects.all().order_by('id')[:10]
    last = ''
    if 'last_login' in request.COOKIES:
        last_login = request.COOKIES.get('last_login','0')
        last = last_login

    return render(request, 'myapp/index.html', {'cat_list': cat_list,'last_login':last})


def about(request):


    about_visits = int(request.COOKIES.get('about_visits', '0'))
    response = render(request, 'myapp/about.html',{'about_visits':about_visits})
    if ('last_visit') in request.COOKIES:

        response.set_cookie('about_visits', about_visits + 1,max_age=300)
    else:

        response.set_cookie('last_visit', '0',max_age=300)
    return response



def cat_no(request, cat_no):
     try:
         warehouse_loc = (Category.objects.get(id=cat_no).warehouse)
     except Category.DoesNotExist:
         raise Http404("Category not found")
     prod_list = get_list_or_404(Product.objects.filter(category__id__contains=cat_no))
    # response = HttpResponse()
    # for location in warehouse_loc:
    #     para1 = '<p>' + 'Location of the  warehouse : ' + str(location[0]) + '</p>'
    #     response.write(para1)
    # for index,products in enumerate(prod_list):
    #     para2 = '<p>' + 'Product ' + str(index+1) + ':' + str(products) + '</p>'
    #     response.write(para2)
    # return response
     return render(request,'myapp/detail.html',{'warehouse_loc': warehouse_loc, 'prod_list': prod_list} )

def products(request):
    prodlist = Product.objects.all().order_by('id')[:10]
    return render(request,'myapp/products.html', {'prodlist': prodlist})

def place_order(request):
    msg = ''
    prodlist = Product.objects.all()
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            if order.num_units <= order.product.stock:

                var = Product.objects.get(name=order.product)
                newstock = Product.objects.filter(name=var).values_list('stock',flat=True).get()
                msg = 'Your order has been placed successfully.'+str(var) +str(order.num_units)+str(newstock)
                p = Product()
                p.updateStock(var,newstock,order.num_units)
                order.save()
            else:
                 msg = 'We do not have sufficient stock to fill your order.'
            return render(request, 'myapp/order_response.html', {'msg': msg})

    else:
        form = OrderForm()
    return render(request, 'myapp/placeorder.html', {'form': form, 'msg': msg,
                                                     'prodlist': prodlist})
def productdetail(request,prod_id):
    product = (Product.objects.get(id=prod_id))

    msg = ''
    #
    # if request.method == 'POST':
    #     form = InterestForm(request.POST)
    #     if form.is_valid():
    #         interest = form.save(commit=False)
    #         p = Product()
    #         if form.interest == 'True':
    #             p.incrementInterested(prod_id)
    #             interest.save()
    #             msg = 'Interest saved successfully'
    #         else:
    #             msg = 'Error'
    #             return request,'myapp/order_response.html',{'msg':msg}
    # else:
    form = InterestForm()
    return render(request,'myapp/productdetails.html', {'product': product, 'form':form, 'msg':msg})

def interest_product(request,prod_id):
    if request.method == 'POST':
        form = InterestForm(request.POST)
        response=HttpResponse()
        if form.is_valid():
            choice=form.cleaned_data['interest']
            if choice:
                p = Product.objects.get(id=prod_id)
                p.incrementInterested(1)
                response.write('success')
                return index(request)
            else:
                response.write('ok not intersted...check out other products?')
            return response
    else:
        return productdetail(request, prod_id)


def user_login(request):
   if request.method == 'POST':
       username = request.POST['username']
       password = request.POST['password']
       user = authenticate(username=username, password=password)
       if user:
            if user.is_active:
                 login(request, user)


                 response =  HttpResponseRedirect(reverse('myapp:index'))
                 response.set_cookie('last_login', datetime.now(), max_age=3600)
                 return response
            else:
                 return HttpResponse('Your account is disabled.')
       else:
            return HttpResponse('Invalid login details.')
   else:
       form = LoginForm()
       return render(request, 'myapp/login.html', {'form':form})

@login_required
def user_logout(request):
    logout(request)
    response =  HttpResponseRedirect(reverse(('myapp:index')))
    response.delete_cookie('last_login')
    return response
