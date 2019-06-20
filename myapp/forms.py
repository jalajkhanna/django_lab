from django import forms
from myapp.models import Order
from django.forms import ModelForm
from django.contrib.auth.models import User


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
    interest = forms.IntegerField(widget=forms.RadioSelect(choices=[(1, 'Yes'),(0, 'No')]))
    quantity = forms.IntegerField(initial=1, min_value=1, label='yolo')
    comments = forms.CharField(widget=forms.Textarea, required=False)

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

# class UserProfile(ModelForm):
#     password = forms.CharField(required=True, widget=forms.PasswordInput)
#     class Meta:
#         model = User
#         fields = ('username','password','email')

