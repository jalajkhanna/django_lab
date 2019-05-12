from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    return render(request, 'index.html')
def about(request):
    return render(request, 'about.html')
def myaccount(request):
    return render(request, 'myaccount.html')
def purchase(request):
    return render(request, 'purchase.html')
def successorder(request):
    return render(request, 'success.html')
