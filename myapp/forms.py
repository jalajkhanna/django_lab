from django import forms
from myapp.models import Order,Client
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = ['client','product','num_units']
        labels = {'client': 'Client Name','num_units': 'Quantity'}

class InterestForm(forms.Form):
    interest = forms.BooleanField(label='I am Interested')
    quantity = forms.IntegerField(initial=1, min_value=1, label='Quantity')
    comments = forms.CharField(widget=forms.Textarea, required=False)

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class SignUpForm(UserCreationForm):

    class Meta:
        model = Client
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2','company', 'shipping_address', 'city', 'province', 'interested_in', 'image' )

