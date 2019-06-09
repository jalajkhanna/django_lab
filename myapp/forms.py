from django import forms
from myapp.models import Order, ModelForm
from django.core.validators import MinValueValidator
# class OrderForm(forms.ModelForm):
#     client = forms.BooleanField()
#     num_units = forms.IntegerField()
#     product = forms.ModelMultipleChoiceField(queryset=Order.objects.values('product__name'))

class OrderForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
        self.fields['client'].empty_label = None

    class Meta:
        model = Order
        fields = ['client','product','num_units']
        labels = {'client': 'Client Name',
                  'num_units': 'Quantity'}
        widgets = {
            'client': forms.RadioSelect
        }

class InterestForm(forms.Form):
    interest = forms.BooleanField(widget=forms.RadioSelect(choices=[(True, 'Yes'),(False, 'No')]))
    quantity = forms.IntegerField(initial=1, validators=MinValueValidator(1))
    comments = forms.CharField(widget=forms.Textarea, required=False)


