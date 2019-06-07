from django import forms
from myapp.models import Order
from django.core.validators import MinValueValidator
class OrderForm(forms.ModelForm):
    client = forms.ModelMultipleChoiceField(queryset=Order.objects.values('client__first_name'), widget=forms.RadioSelect, label='Client Name')
    num_units = forms.IntegerField(label='Quantity')
    product = forms.ModelMultipleChoiceField(queryset=Order.objects.values('product__name'))

class InterestForm(forms.Form):
    interest = forms.BooleanField(widget=forms.RadioSelect(choices=[(True, 'Yes'),(False, 'No')]))
    quantity = forms.IntegerField(default=1, validators=MinValueValidator(1))
    comments = forms.CharField(label='Additional Comments', widget=forms.Textarea, required=False)
