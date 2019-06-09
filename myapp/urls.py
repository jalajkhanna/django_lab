from django.urls import path, re_path
from django.conf.urls import url

from myapp import views

# urlpatterns = [
#     path('', views.index, name='index'),
#     path('about',views.about, name='about'),
#     path('purchase', views.purchase, name='purchase'),
#     path('myaccount', views.myaccount, name='myaccount'),
#     path('successorder', views.successorder, name='successorder'),
#     path('clothing', views.clothing, name='clothing'),
#     path('equipment', views.equipment, name='equipment'),
#     path('otheritem', views.otheritem, name='otheritem'),
#     path('productdetails', views.productdetails, name='productdetails')
#
# ]

app_name = 'myapp'
urlpatterns = [ path(r'', views.index, name='index'),
                path(r'about/',views.about, name='about'),
                path('cat_no/<int:cat_no>/', views.cat_no),
                path(r'products/',views.products,name='products'),
                path(r'placeorder/',views.place_order,name='place order'),
                path(r'order_response/',views.place_order,name='order response')]
