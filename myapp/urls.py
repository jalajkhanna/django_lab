from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about',views.about, name='about'),
    path('purchase', views.purchase, name='purchase'),
    path('myaccount', views.myaccount, name='myaccount')
]