from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.utils.datetime_safe import datetime

from .models import Category, Product, Client, Order
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from myapp.forms import OrderForm, InterestForm, LoginForm, SignUpForm
from django.urls import reverse
from django.core.mail import send_mail
from django.conf import settings

def index(request):
    cat_list = Category.objects.all().order_by('id')[:10]
    if request.session.get('last_login_time', False):
        last=request.session.get('last_login_time')
    else:
        return render(request, 'myapp/index.html', {'cat_list': cat_list, 'last_login': 'last login more than 1 hour'})
    return render(request, 'myapp/index.html', {'cat_list': cat_list,'last_login':'last login time:' + last})


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
     return render(request,'myapp/detail.html',{'warehouse_loc': warehouse_loc, 'prod_list': prod_list} )

def products(request):
    prodlist = Product.objects.all().order_by('id')
    return render(request,'myapp/products.html', {'prodlist': prodlist})


@login_required(login_url='/myapp/user_login/')
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
                msg = 'Your order has been placed successfully.'
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
                request.session['username']=username
                request.session['last_login_time']=str(datetime.now())
                request.session.set_expiry(3600)
                if 'next' in request.POST:
                     return redirect(request.POST.get('next'))
                else:
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
    return HttpResponseRedirect(reverse(('myapp:index')))

@login_required(login_url='/myapp/user_login/')
def myorders(request):
        name = request.user.first_name
        orders = Order.objects.filter(client__first_name=name).values_list('product__name',flat=True)
        return render(request,'myapp/myorders.html',{'orders':orders})


def register(request):
    if request.method== 'POST':
        form = SignUpForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            pwd = form.cleaned_data.get('password1')
            user=authenticate(username=username,password=pwd)
            login(request,user)
            return HttpResponseRedirect(reverse(('myapp:index')))
        else:
            return HttpResponse('Invalid')
    form = SignUpForm()
    return render(request,'myapp/register.html',{'form':form})


def email(request):
    subject = 'Thank you for registering to our site'
    message = ' it  means a world to us '
    email_from = settings.EMAIL_HOST_USER
    recipient_list = ['jalaj.khanna@gmail.com',]
    send_mail( 'yo', 'test', settings.EMAIL_HOST_USER, ['jalaj.khanna@gmail.com'] )
    return HttpResponseRedirect(reverse(('myapp:index')))


