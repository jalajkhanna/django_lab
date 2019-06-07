from django import forms
from myapp.models import Order

class OrderForm(forms.ModelForm):
    client = forms.ModelMultipleChoiceField(queryset=Order.objects.values('client__first_name'), widget=forms.RadioSelect, label='Client Name')
    num_units = forms.IntegerField(label='Quantity')
    product = forms.ModelMultipleChoiceField(queryset=Order.objects.values('product__name'))
